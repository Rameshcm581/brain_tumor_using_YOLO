from sqlalchemy import Column, Integer, String, Date, ForeignKey,DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(500))

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100))
    attender_name = Column(String(100))
    dob = Column(Date)
    age = Column(Integer)
    gender = Column(String(10))
    mobile = Column(String(15))
    city = Column(String(50))
    images = relationship("MedicalImage", backref="patient")
    created_by = Column(Integer, ForeignKey("users.id"))
    
class MedicalImage(Base):
    __tablename__ = "medical_images"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    image_path = Column(String(500))  # Original image URL
    processed_image_path = Column(String(500))  # Processed image URL
    upload_date = Column(DateTime, default=datetime.now)
    analysis_result = Column(String(200))
