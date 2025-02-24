# YOLO Object Detection with Streamlit

The **YOLO Object Detection with Streamlit** is a Python-based application that uses the YOLO (You Only Look Once) model for object detection in images. It provides a user-friendly interface built with Streamlit, allowing users to select a YOLO model from a local folder, upload an image, and run object detection. The application displays the original image alongside the annotated image with detected objects.

## Features

- **Model Selection**: Users can select a YOLO model from a local folder containing `.pt` files.
- **Image Upload**: Users can upload images in JPG, JPEG, or PNG formats.
- **Object Detection**: The application runs YOLO object detection on the uploaded image and displays the results.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and interactive experience.

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For the graphical user interface (GUI).
- **YOLO (Ultralytics)**: For object detection.
- **Pillow (PIL)**: For image processing.
- **NumPy**: For handling image data as arrays.

## Installation

### Prerequisites

1. **Python 3.8 or higher**: Download and install Python from [python.org](https://www.python.org/).
2. **Git**: Install Git from [git-scm.com](https://git-scm.com/).

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Rameshcm581/brain_tumor_using_YOLO.git
   cd brain_tumor_using_YOLO
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare the Models Folder**:
   - Create a folder named `Model/Types` in the project directory.
   - Place your YOLO model files (`.pt`) in this folder.

5. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Usage

### 1. **Select a YOLO Model**
   - Use the dropdown menu to select a YOLO model from the `Model/Types` folder.

### 2. **Upload an Image**
   - Upload an image in JPG, JPEG, or PNG format using the file uploader.

### 3. **Run Object Detection**
   - Click the "Run YOLO Detection" button to perform object detection on the uploaded image.
   - The application will display the original image alongside the annotated image with detected objects.

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the GUI framework.
- [YOLO (Ultralytics)](https://ultralytics.com/) for object detection.
- [Pillow (PIL)](https://pillow.readthedocs.io/) for image processing.
- [NumPy](https://numpy.org/) for handling image data as arrays.

---

## Contact

For any questions or feedback, feel free to reach out:

- **Email**: [rameshc182003@gamil.com](rameshc182003@gmail.com)
- **GitHub**: [Rameshcm581](https://github.com/Rameshcm581)

---
