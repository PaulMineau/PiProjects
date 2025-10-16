# Animal Classification Web App

A Streamlit-based web application that uses computer vision to classify animals in uploaded images. Built for Raspberry Pi deployment using OpenCV and a pre-trained MobileNetV2 model.

## Features

- 🖼️ **Image Upload**: Drag-and-drop or browse to upload images
- 🧠 **AI Classification**: Identifies animals using a pre-trained deep learning model
- 📊 **Confidence Scores**: Shows prediction confidence levels
- 🔧 **Configurable Threshold**: Adjustable confidence threshold
- 📱 **Responsive UI**: Works on desktop and mobile devices
- 🔍 **Processing Details**: Optional detailed analysis view
- 📈 **System Monitoring**: Real-time CPU and memory usage

## Supported Animals

The app can identify various animals including:
- Dogs 🐕 (multiple breeds)
- Cats 🐱 (domestic and wild)
- Birds 🐦 (various species)
- Horses 🐴
- Farm animals (sheep, cows, etc.)
- Wild animals (elephants, bears, zebras, giraffes)
- And many more from the ImageNet dataset

## Installation

### Prerequisites
- Python 3.7 or higher
- At least 2GB RAM (recommended for model inference)
- Network connectivity for downloading the pre-trained model

### Local Installation
```bash
# Clone the repository
git clone <repository-url>
cd src

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run animal_classifier.py
```

### Raspberry Pi Installation
```bash
# Update system
sudo apt update

# Install system dependencies
sudo apt install -y python3-pip python3-venv
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libatlas-base-dev libhdf5-dev

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run the application (accessible on network)
streamlit run animal_classifier.py --server.port 8501 --server.address 0.0.0.0
```

## Usage

1. **Start the Application**: Run the Streamlit app using the command above
2. **Access the Interface**: Open your browser to `http://localhost:8501`
3. **Upload an Image**: Use the file uploader or try a sample image
4. **View Results**: The app will display:
   - The uploaded image
   - Classification result
   - Confidence score
   - Processing time
5. **Adjust Settings**: Use the sidebar to modify confidence threshold and view options

## Project Structure

```
src/
├── animal_classifier.py      # Main Streamlit application
├── models/
│   └── model_utils.py        # Model loading and inference
├── utils/
│   └── image_processing.py   # Image preprocessing utilities
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── sample_images/           # Sample test images (optional)
```

## Configuration

### Confidence Threshold
- Adjust the confidence threshold in the sidebar (0.1 - 0.9)
- Higher values = more strict classification
- Lower values = more permissive classification

### System Requirements
- **Memory**: ~500MB RAM during inference
- **CPU**: Any modern CPU (optimized for ARM on Raspberry Pi)
- **Storage**: ~2GB for model and dependencies

## Troubleshooting

### Memory Issues
```bash
# Increase swap on Raspberry Pi
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### OpenCV Issues
```bash
# Alternative OpenCV installation
pip install opencv-python-headless
```

### Port Already in Use
```bash
# Check what's using port 8501
sudo netstat -tlnp | grep :8501

# Kill process if needed
sudo lsof -t -i tcp:8501 | xargs kill -9
```

## Performance Notes

- **First run** may take longer due to model download
- **Processing time**: 2-5 seconds per image on Pi 4
- **Model size**: ~14MB (MobileNetV2)
- **Best results**: Clear, well-lit images with animals as main subject

## API Usage

The classification functions can also be used programmatically:

```python
from models.model_utils import AnimalClassifier
from utils.image_processing import preprocess_image

# Initialize classifier
classifier = AnimalClassifier()

# Load and preprocess image
image = preprocess_image("path/to/your/image.jpg")

# Classify
result = classifier.classify(image)
print(f"Animal: {result['animal']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.