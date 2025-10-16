# Tutorial 03: Animal Classification Web App for Raspberry Pi

## Overview
This tutorial will guide you through creating a computer vision web application that uses OpenCV and a pre-trained model to classify animals in uploaded images. The app runs on Streamlit and is optimized for Raspberry Pi.

## What We'll Build
- Streamlit web application for image upload
- OpenCV-based animal classification using a pre-trained model
- Real-time image processing and classification
- User-friendly interface with image preview and results

## Prerequisites
- Raspberry Pi with SSH access
- Python 3.7 or higher
- At least 2GB of available RAM (recommended for model inference)
- Network connectivity for downloading the pre-trained model

## Project Structure
```
src/
├── animal_classifier.py    # Main Streamlit application
├── models/
│   └── model_utils.py      # Model loading and inference utilities
├── utils/
│   └── image_processing.py # Image preprocessing utilities
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── sample_images/         # Sample test images (optional)
```

## Features
- **Image Upload**: Drag-and-drop or browse to upload images
- **Animal Classification**: Detects common animals or returns "no animal"
- **Confidence Scores**: Shows prediction confidence
- **Image Preview**: Displays uploaded image with results
- **Pi Optimized**: Lightweight model suitable for Raspberry Pi hardware

## Model Information
This app uses a pre-trained MobileNetV2 model fine-tuned for animal classification, which is lightweight and suitable for Raspberry Pi hardware.

## Installation Steps

### 1. Transfer files to your Pi
```bash
# From your local machine
scp -r src/ yourusername@your-pi-ip:~/animal-classifier/
```

### 2. SSH into your Pi and set up the environment
```bash
ssh yourusername@your-pi-ip
cd ~/animal-classifier
```

### 3. Install dependencies
```bash
# Update system
sudo apt update

# Install system dependencies for OpenCV
sudo apt install -y python3-pip python3-venv
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev
sudo apt install -y libatlas-base-dev libjasper-dev libqtgui4 libqt4-test

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 4. Run the application
```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run animal_classifier.py --server.port 8501 --server.address 0.0.0.0
```

### 5. Access the application
- **Local access**: http://localhost:8501
- **Network access**: http://YOUR_PI_IP:8501

## Usage Instructions

1. **Upload an Image**: Click "Browse files" or drag and drop an image
2. **View Results**: The app will process the image and show:
   - Uploaded image preview
   - Classification result (animal type or "no animal")
   - Confidence score
   - Processing time

3. **Supported Formats**: JPG, JPEG, PNG, BMP

## Performance Notes
- **First Run**: May take longer due to model download and initialization
- **Processing Time**: 2-5 seconds per image on Pi 4, longer on older models
- **Memory Usage**: ~500MB RAM during inference
- **Supported Animals**: Dog, Cat, Bird, Horse, Sheep, Cow, Elephant, Bear, Zebra, Giraffe, and more

## Troubleshooting

### Memory Issues
```bash
# Increase swap if needed
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Set CONF_SWAPSIZE=1024
sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### OpenCV Installation Issues
```bash
# Alternative OpenCV installation
pip install opencv-python-headless
```

### Streamlit Port Issues
```bash
# Check if port is in use
sudo netstat -tlnp | grep :8501

# Kill process if needed
sudo lsof -t -i tcp:8501 | xargs kill -9
```

## Customization Options

### Adding New Animal Classes
Edit `models/model_utils.py` to modify the classification labels.

### Adjusting Confidence Threshold
Modify the confidence threshold in `animal_classifier.py` to make classifications more or less strict.

### UI Customization
Streamlit allows extensive UI customization through the main application file.

## API Endpoints
While this is primarily a Streamlit app, you can also use the classification functions programmatically by importing from the modules.

---

**Ready to classify some animals! 🐾**