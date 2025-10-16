#!/usr/bin/env python3
"""
Animal Classification Web App
A Streamlit application that uses OpenCV and a pre-trained model to classify animals in uploaded images.
Optimized for Raspberry Pi deployment.
"""

import streamlit as st
import cv2
import numpy as np
import time
from PIL import Image
import io
import os
import sys

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.model_utils import AnimalClassifier
from utils.image_processing import preprocess_image, resize_image

# Page configuration
st.set_page_config(
    page_title="🐾 Animal Classifier",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 3rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #2E8B57;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #228B22;
    }
    .result-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the classifier
@st.cache_resource
def load_classifier():
    """Load the animal classifier model (cached for performance)"""
    try:
        classifier = AnimalClassifier()
        return classifier
    except Exception as e:
        st.error(f"Error loading classifier: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🐾 Animal Classifier</h1>', unsafe_allow_html=True)
    st.markdown("### Upload an image to classify what type of animal it contains!")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
        This app uses a pre-trained computer vision model to classify animals in uploaded images.
        
        **Supported Animals:**
        - Dogs 🐕
        - Cats 🐱
        - Birds 🐦
        - Horses 🐴
        - Sheep 🐑
        - Cows 🐄
        - Elephants 🐘
        - Bears 🐻
        - Zebras 🦓
        - Giraffes 🦒
        - And more!
        """)
        
        st.header("🔧 Settings")
        confidence_threshold = st.slider(
            "Confidence Threshold", 
            min_value=0.1, 
            max_value=0.9, 
            value=0.5, 
            step=0.1,
            help="Minimum confidence required for classification"
        )
        
        show_processing_details = st.checkbox("Show processing details", value=False)
        
        st.header("📊 System Info")
        if st.button("Refresh System Info"):
            st.rerun()
        
        # Display system information
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            
            st.metric("CPU Usage", f"{cpu_percent:.1f}%")
            st.metric("Memory Usage", f"{memory_info.percent:.1f}%")
            st.metric("Available Memory", f"{memory_info.available // (1024*1024)} MB")
        except ImportError:
            st.info("Install psutil for system monitoring: `pip install psutil`")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Image")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload an image containing an animal for classification"
        )
        
        # Sample images section
        st.subheader("🖼️ Or try a sample image")
        sample_option = st.selectbox(
            "Select a sample:",
            ["None", "Dog", "Cat", "Bird", "Horse", "No Animal"],
            help="Choose a sample image to test the classifier"
        )
        
        sample_image = None
        if sample_option != "None":
            # Generate a simple colored rectangle as a placeholder
            # In a real implementation, you'd have actual sample images
            sample_image = generate_sample_image(sample_option)
            st.image(sample_image, caption=f"Sample: {sample_option}", use_column_width=True)
            
            if st.button("Classify Sample Image"):
                # Store sample image in session state for processing
                st.session_state['sample_image'] = sample_image
    
    with col2:
        st.subheader("🔍 Classification Results")
        
        # Check for sample image in session state
        if 'sample_image' in st.session_state:
            uploaded_file = st.session_state['sample_image']
            # Clear sample image after use
            del st.session_state['sample_image']
        
        if uploaded_file is not None:
            try:
                # Load and display the image
                if isinstance(uploaded_file, np.ndarray):
                    # Sample image case
                    image = uploaded_file
                    pil_image = Image.fromarray(image)
                else:
                    # Uploaded file case
                    image = Image.open(uploaded_file)
                    pil_image = image
                    image = np.array(image)
                
                st.image(pil_image, caption="Uploaded Image", use_column_width=True)
                
                # Process the image
                with st.spinner("🧠 Analyzing image..."):
                    start_time = time.time()
                    
                    # Load classifier
                    classifier = load_classifier()
                    if classifier is None:
                        st.error("Failed to load the classification model. Please check the logs.")
                        return
                    
                    # Preprocess image
                    if show_processing_details:
                        st.info("Preprocessing image...")
                    
                    processed_image = preprocess_image(image)
                    
                    # Classify the image
                    if show_processing_details:
                        st.info("Running classification...")
                    
                    result = classifier.classify(processed_image)
                    
                    processing_time = time.time() - start_time
                
                # Display results
                if result['confidence'] >= confidence_threshold:
                    st.markdown(f"""
                    <div class="result-box success-box">
                        <h3>🎉 Classification Result</h3>
                        <p><strong>Animal Detected:</strong> {result['animal']}</p>
                        <p><strong>Confidence:</strong> {result['confidence']:.2%}</p>
                        <p><strong>Processing Time:</strong> {processing_time:.2f} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show confidence bar
                    st.progress(result['confidence'])
                    
                else:
                    st.markdown(f"""
                    <div class="result-box warning-box">
                        <h3>🤔 Classification Result</h3>
                        <p><strong>Result:</strong> No animal detected (low confidence)</p>
                        <p><strong>Best Guess:</strong> {result['animal']} ({result['confidence']:.2%})</p>
                        <p><strong>Processing Time:</strong> {processing_time:.2f} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show processing details if requested
                if show_processing_details:
                    with st.expander("🔧 Processing Details"):
                        st.write("**Original Image Shape:**", image.shape)
                        st.write("**Processed Image Shape:**", processed_image.shape)
                        st.write("**Model Input Shape:**", classifier.get_input_shape())
                        st.write("**All Predictions:**")
                        
                        # Show top 5 predictions
                        top_predictions = result.get('all_predictions', [])[:5]
                        for i, (animal, conf) in enumerate(top_predictions, 1):
                            st.write(f"{i}. {animal}: {conf:.2%}")
                
                # Additional actions
                st.subheader("📋 Actions")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("🔄 Classify Again"):
                        st.rerun()
                
                with col_b:
                    if st.button("📊 View Details", key="details"):
                        show_image_details(image, result)
                        
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
                if show_processing_details:
                    st.exception(e)
        
        else:
            st.markdown("""
            <div class="result-box info-box">
                <h3>👆 Upload an image to get started</h3>
                <p>Select an image file using the upload button on the left, or choose a sample image to test the classifier.</p>
            </div>
            """, unsafe_allow_html=True)

def generate_sample_image(animal_type):
    """Generate a simple colored rectangle as a sample image placeholder"""
    colors = {
        "Dog": [139, 69, 19],      # Brown
        "Cat": [255, 165, 0],      # Orange
        "Bird": [135, 206, 235],   # Sky blue
        "Horse": [160, 82, 45],    # Saddle brown
        "No Animal": [128, 128, 128]  # Gray
    }
    
    color = colors.get(animal_type, [128, 128, 128])
    image = np.full((300, 300, 3), color, dtype=np.uint8)
    
    # Add text to the image
    cv2.putText(image, animal_type, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return image

def show_image_details(image, result):
    """Show detailed information about the image and classification"""
    st.subheader("📊 Detailed Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Image Information:**")
        st.write(f"- Dimensions: {image.shape[1]} x {image.shape[0]} pixels")
        st.write(f"- Channels: {image.shape[2] if len(image.shape) > 2 else 1}")
        st.write(f"- Data type: {image.dtype}")
        st.write(f"- Size: {image.nbytes / 1024:.1f} KB")
    
    with col2:
        st.write("**Classification Details:**")
        st.write(f"- Predicted: {result['animal']}")
        st.write(f"- Confidence: {result['confidence']:.2%}")
        st.write(f"- Threshold: {st.session_state.get('confidence_threshold', 0.5):.1%}")

if __name__ == "__main__":
    main()