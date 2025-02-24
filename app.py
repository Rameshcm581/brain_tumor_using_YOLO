import streamlit as st
import os
from PIL import Image
import numpy as np
from ultralytics import YOLO

def run_yolo(image_np, model_path):
    """
    Load the YOLO model from the given path, run inference on the image,
    and return the annotated image.
    """
    model = YOLO(model_path)
    results = model(image_np)
    annotated_frame = results[0].plot()
    return annotated_frame

def main():
    st.title("YOLO Object Detection with Streamlit")
    st.write("First, select a YOLO model from the local 'models' folder, then upload an image for detection.")

    # Define the folder containing the models
    model_folder = "./Model/Types"
    
    # List all .pt files in the models folder
    if os.path.exists(model_folder):
        available_models = [f for f in os.listdir(model_folder) if f.endswith('.pt')]
    else:
        available_models = []
        st.error(f"Model folder '{model_folder}' not found. Please create it and add your .pt files.")

    # Add a placeholder option so the user must explicitly select a model
    model_options = ["Select a model"] + available_models
    selected_model = st.selectbox("Select YOLO Model", model_options)

    if selected_model == "Select a model":
        st.warning("Please select a YOLO model from the dropdown above to proceed.")
    else:
        # Only display the uploader if a valid model is selected
        uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Convert the image to a NumPy array
            image_np = np.array(image)
            
            # Run detection on button press
            if st.button("Run YOLO Detection"):
                model_path = os.path.join(model_folder, selected_model)
                st.write("Running inference...")
                output_image = run_yolo(image_np, model_path)
                st.image(output_image, caption="YOLO Output", use_column_width=True)

if __name__ == "__main__":
    main()
