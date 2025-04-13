from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker, Session
import os
import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ultralytics import YOLO
from contextlib import asynccontextmanager
import models
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configure Cloudinary (add to your app startup)
cloudinary.config(
    cloud_name='dlrhlfds6',
    api_key='475288642736875',
    api_secret='xlRh-aNsFoAtWwxLxZJghIU_wRA'
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("static/uploads", exist_ok=True)
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key="your_secret_key_here_keep_it_secure",
    session_cookie="medsession",
    max_age=3600  # Optional: session expiration time
)

# Database setup
DATABASE_URL = "postgresql://neondb_owner:npg_9P1ocOmQjfTZ@ep-red-unit-a1hj0zl3.ap-southeast-1.aws.neon.tech/tumor_imaging?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Templates and static files
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static_files")

# YOLO model
model = YOLO('models/best.pt')


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username_email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(or_(
        models.User.username == username_email,
        models.User.email == username_email
    )).first()

    if not user or not check_password_hash(user.password, password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username/email or password"
        })
    
    request.session["user_id"] = user.id
    request.session["user_email"] = user.email
    return RedirectResponse("/patient", status_code=303)

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(or_(
        models.User.username == username,
        models.User.email == email
    )).first()
    
    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Username or email already exists"
        })
    
    new_user = models.User(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse("/login", status_code=303)

@app.get("/patient", response_class=HTMLResponse)
async def patient_page(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("patient.html", {"request": request})

@app.post("/patient", response_class=HTMLResponse)
async def create_patient(
    request: Request,
    fullname: str = Form(...),
    attendername: str = Form(...),  # Must match HTML name attribute
    dob: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    mobile: str = Form(...),
    city: str = Form(...),
    db: Session = Depends(get_db)
):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=303)
    
    try:
        dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        new_patient = models.Patient(
            fullname=fullname,
            attender_name=attendername,  # Must match model field name
            dob=dob_date,
            age=age,
            gender=gender,
            mobile=mobile,
            city=city,
            created_by=request.session["user_id"]
        )
        db.add(new_patient)
        db.commit()  # Ensure this is called
        db.refresh(new_patient)  # Optional but recommended
    except Exception as e:
        db.rollback()
        print(f"Database error: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))
    
    request.session["current_patient_id"] = new_patient.id
    
    return RedirectResponse("/upload", status_code=303)

@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def analyze_image(
    request: Request,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if "user_id" not in request.session or "current_patient_id" not in request.session:
        return RedirectResponse("/login", status_code=303)
    
    try:
        start_time = time.time()
        patient_id = request.session["current_patient_id"]

        # 1. Save uploaded file temporarily
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, image.filename)
        
        with open(temp_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)

        # 2. Process with YOLO using local file
        results = model(temp_path)
        
        # 3. Save processed image temporarily
        processed_filename = f"processed_{image.filename}"
        processed_path = os.path.join(temp_dir, processed_filename)
        results[0].save(processed_path)

        # 4. Upload both images to Cloudinary
        original_upload = cloudinary.uploader.upload(
            temp_path,
            folder="medical_images/original",
            public_id=f"patient_{patient_id}_{int(time.time())}",
            resource_type="image"
        )
        
        processed_upload = cloudinary.uploader.upload(
            processed_path,
            folder="medical_images/processed",
            public_id=f"patient_{patient_id}_{int(time.time())}",
            resource_type="image"
        )

        # 5. Clean up temp files
        os.remove(temp_path)
        os.remove(processed_path)

        # 6. Store results in database
        new_image = models.MedicalImage(
            patient_id=patient_id,
            image_path=original_upload['secure_url'],
            processed_image_path=processed_upload['secure_url'],
            analysis_result=", ".join([model.names[int(cls)] for cls in results[0].boxes.cls]) if results[0].boxes.cls else None
        )
        db.add(new_image)
        db.commit()

        processing_time = round(time.time() - start_time, 2)
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "image_path": processed_upload['secure_url'],
            "analysis_date": datetime.now(),
            "processing_time": processing_time,
            "diagnosis_result": new_image.analysis_result
        })
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
