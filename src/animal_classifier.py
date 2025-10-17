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

# Fixed imports
from models.model_utils import AnimalClassifier
from utils.image_processing import ImageProcessor

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
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# Initialize the classifier and image processor
@st.cache_resource
def load_models():
    """Load the animal classifier and image processor (cached for performance)"""
    try:
        classifier = AnimalClassifier()
        processor = ImageProcessor()
        return classifier, processor
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🐾 Animal Classifier</h1>', unsafe_allow_html=True)
    st.markdown("### Upload an image to classify what type of animal it contains!")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
        This app uses a pre-trained MobileNetV2 model to classify animals in uploaded images.
        
        **Supported Animals:**
        - Dogs & Wolves 🐕🐺
        - Cats & Big Cats 🐱🦁
        - Birds 🐦
        - Horses & Zebras 🐴🦓
        - Farm Animals 🐄🐑🐷
        - Wild Animals 🐘🐻🦒
        - Marine Animals 🐋🐟
        - And many more!
        """)
        
        st.header("🔧 Settings")
        confidence_threshold = st.slider(
            "Confidence Threshold", 
            min_value=0.05, 
            max_value=0.95, 
            value=0.1, 
            step=0.05,
            help="Minimum confidence required for animal classification"
        )
        
        show_processing_details = st.checkbox("Show processing details", value=False)
        show_all_predictions = st.checkbox("Show all predictions", value=False)
        
        # Debug options for wolf detection
        st.subheader("🐺 Wolf Detection Debug")
        force_animal_check = st.checkbox("Force animal analysis (ignore confidence)", value=False)
        show_top_20_predictions = st.checkbox("Show top 20 predictions", value=False)
        try_alternative_preprocessing = st.checkbox("Try alternative preprocessing", value=False)
        auto_crop = st.checkbox("Auto-crop main subject", value=False)
        
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
            ["None", "Wolf/Dog", "Cat", "Bird", "Horse", "Bear", "Elephant", "No Animal"],
            help="Choose a sample image to test the classifier"
        )
        
        if sample_option != "None":
            sample_image = generate_sample_image(sample_option)
            st.image(sample_image, caption=f"Sample: {sample_option}", use_column_width=True)
            
            if st.button("Classify Sample Image"):
                st.session_state['process_image'] = sample_image
    
    with col2:
        st.subheader("🔍 Classification Results")
        
        # Determine which image to process
        image_to_process = None
        image_source = ""
        
        if uploaded_file is not None:
            image_to_process = uploaded_file
            image_source = "uploaded"
        elif 'process_image' in st.session_state:
            image_to_process = st.session_state['process_image']
            image_source = "sample"
            del st.session_state['process_image']
        
        if image_to_process is not None:
            try:
                # Load and display the image
                if isinstance(image_to_process, np.ndarray):
                    # Sample image case
                    image_array = image_to_process
                    pil_image = Image.fromarray(image_array)
                else:
                    # Uploaded file case
                    pil_image = Image.open(image_to_process)
                    image_array = np.array(pil_image)
                
                st.image(pil_image, caption=f"{image_source.title()} Image", use_column_width=True)
                
                # Process the image
                with st.spinner("🧠 Analyzing image..."):
                    start_time = time.time()
                    
                    # Load models
                    classifier, processor = load_models()
                    if classifier is None or processor is None:
                        st.error("Failed to load the classification models. Please check the logs.")
                        return
                    
                    # Enhanced preprocessing with multiple strategies
                    if show_processing_details:
                        st.info("Preprocessing image with enhanced strategies...")
                    
                    # Strategy 1: Standard enhanced preprocessing
                    processed_image_1 = processor.preprocess_image(image_array, target_size=(224, 224), enhance=True)
                    
                    # Strategy 2: Alternative preprocessing if enabled
                    processed_image_2 = None
                    processed_image_3 = None
                    if try_alternative_preprocessing:
                        processed_image_2 = processor.preprocess_image(image_array, target_size=(224, 224), enhance=False)
                        # Try with auto-crop too
                        if auto_crop:
                            cropped_image = processor.detect_and_crop_main_subject(image_array)
                            processed_image_3 = processor.preprocess_image(cropped_image, target_size=(224, 224), enhance=True)
                    
                    # Get predictions for all strategies
                    if show_processing_details:
                        st.info("Getting predictions with multiple strategies...")
                    
                    # Strategy 1: Enhanced preprocessing
                    predictions_1 = classifier.predict(processed_image_1, top_k=20 if show_top_20_predictions else 10)
                    is_animal_1, animal_type_1, confidence_1 = classifier.classify_animal(
                        processed_image_1, confidence_threshold=0.01 if force_animal_check else confidence_threshold
                    )
                    
                    # Use best strategy
                    predictions = predictions_1
                    is_animal, animal_type, confidence = is_animal_1, animal_type_1, confidence_1
                    processed_image = processed_image_1
                    strategy_used = "Enhanced preprocessing"
                    
                    # Try alternative strategies if enabled
                    if try_alternative_preprocessing and processed_image_2 is not None:
                        predictions_2 = classifier.predict(processed_image_2, top_k=20 if show_top_20_predictions else 10)
                        is_animal_2, animal_type_2, confidence_2 = classifier.classify_animal(
                            processed_image_2, confidence_threshold=0.01 if force_animal_check else confidence_threshold
                        )
                        
                        # Check if alternative gives better animal detection
                        if (is_animal_2 and not is_animal_1) or (is_animal_2 and confidence_2 > confidence_1):
                            predictions = predictions_2
                            is_animal, animal_type, confidence = is_animal_2, animal_type_2, confidence_2
                            processed_image = processed_image_2
                            strategy_used = "Standard preprocessing"
                        
                        # Try cropped version if enabled
                        if auto_crop and processed_image_3 is not None:
                            predictions_3 = classifier.predict(processed_image_3, top_k=20 if show_top_20_predictions else 10)
                            is_animal_3, animal_type_3, confidence_3 = classifier.classify_animal(
                                processed_image_3, confidence_threshold=0.01 if force_animal_check else confidence_threshold
                            )
                            
                            if (is_animal_3 and not is_animal) or (is_animal_3 and confidence_3 > confidence):
                                predictions = predictions_3
                                is_animal, animal_type, confidence = is_animal_3, animal_type_3, confidence_3
                                processed_image = processed_image_3
                                strategy_used = "Cropped + enhanced"
                    
                    # Show image info if processing details enabled
                    if show_processing_details:
                        image_info = processor.get_image_info(processed_image)
                        st.info(f"Strategy: {strategy_used} | Size: {image_info['width']}x{image_info['height']} | Brightness: {image_info.get('brightness', 0):.1f}")
                    
                    # Manual wolf detection check
                    wolf_indicators = ['wolf', 'timber', 'gray', 'grey', 'canine', 'lupus', 'dog', 'husky', 'malamute']
                    likely_wolf = any(indicator in pred[0].lower() for pred in predictions[:10] for indicator in wolf_indicators)
                    
                    # Enhanced animal classification with forced checking
                    if force_animal_check or likely_wolf:
                        # Force re-evaluate as potential animal
                        for class_name, conf in predictions[:15]:
                            if any(indicator in class_name.lower() for indicator in wolf_indicators):
                                is_animal = True
                                animal_type = f"{class_name} (wolf detected)"
                                confidence = conf
                                break
                        
                        # If still not detected but spotlight with reasonable confidence, assume wolf
                        if not is_animal and "spotlight" in predictions[0][0].lower() and predictions[0][1] > 0.05:
                            is_animal = True
                            animal_type = "Possible Wolf (misclassified as spotlight)"
                            confidence = predictions[0][1]
                    
                    processing_time = time.time() - start_time
                
                # Display results
                if is_animal and confidence >= confidence_threshold:
                    st.markdown(f"""
                    <div class="result-box success-box">
                        <h3>🎉 Animal Detected!</h3>
                        <p><strong>Animal Type:</strong> {animal_type}</p>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                        <p><strong>Processing Time:</strong> {processing_time:.2f} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show confidence bar
                    st.progress(float(confidence))
                    
                elif is_animal:
                    st.markdown(f"""
                    <div class="result-box warning-box">
                        <h3>🤔 Possible Animal (Low Confidence)</h3>
                        <p><strong>Possible Type:</strong> {animal_type}</p>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                        <p><strong>Threshold:</strong> {confidence_threshold:.2%}</p>
                        <p><strong>Processing Time:</strong> {processing_time:.2f} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show confidence bar for low confidence too
                    st.progress(float(confidence))
                else:
                    st.markdown(f"""
                    <div class="result-box info-box">
                        <h3>📷 No Animal Detected</h3>
                        <p><strong>Top Prediction:</strong> {animal_type}</p>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                        <p><strong>Processing Time:</strong> {processing_time:.2f} seconds</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Show all predictions if requested
                if show_all_predictions or show_processing_details or show_top_20_predictions:
                    with st.expander("📊 All Model Predictions"):
                        pred_count = 20 if show_top_20_predictions else 10
                        st.write(f"**Top {pred_count} Predictions:**")
                        
                        for i, (class_name, conf) in enumerate(predictions[:pred_count], 1):
                            # Enhanced animal detection highlighting
                            animal_keywords = ['dog', 'cat', 'wolf', 'fox', 'bear', 'bird', 'horse', 'cow', 'sheep', 'pig', 'deer', 'rabbit']
                            wolf_keywords = ['wolf', 'timber', 'gray', 'grey', 'canine', 'lupus', 'husky', 'malamute']
                            
                            is_pred_animal = any(keyword in class_name.lower() for keyword in animal_keywords)
                            is_wolf_like = any(keyword in class_name.lower() for keyword in wolf_keywords)
                            
                            if is_wolf_like:
                                marker = "🐺"
                                style = "**🐺 WOLF-LIKE**"
                            elif is_pred_animal:
                                marker = "🐾"
                                style = "**"
                            else:
                                marker = "📷"
                                style = ""
                            
                            st.write(f"{marker} {i:2d}. {style}{class_name}{style}: {conf:.2%}")
                            
                            # Special highlighting for spotlight
                            if "spotlight" in class_name.lower() and i <= 3:
                                st.warning(f"⚠️ '{class_name}' detected - this might be a wolf misclassified due to lighting/eyes!")
                
                # Enhanced processing details
                if show_processing_details:
                    with st.expander("🔧 Enhanced Processing Details"):
                        st.write("**Strategy Information:**")
                        st.write(f"- Processing Strategy: {strategy_used}")
                        st.write(f"- Force Animal Check: {force_animal_check}")
                        st.write(f"- Alternative Preprocessing: {try_alternative_preprocessing}")
                        st.write(f"- Auto Crop: {auto_crop}")
                        
                        st.write("**Image Information:**")
                        st.write(f"- Original Shape: {image_array.shape}")
                        st.write(f"- Processed Shape: {processed_image.shape}")
                        st.write(f"- Image Size: {image_array.nbytes / 1024:.1f} KB")
                        
                        # Check for wolf-like predictions
                        wolf_predictions = [pred for pred in predictions[:10] 
                                          if any(w in pred[0].lower() for w in ['wolf', 'dog', 'canine', 'lupus'])]
                        if wolf_predictions:
                            st.write("**🐺 Wolf-like Predictions Found:**")
                            for pred in wolf_predictions:
                                st.write(f"   - {pred[0]}: {pred[1]:.2%}")
                        
                        st.write("**Model Information:**")
                        st.write(f"- Model: MobileNetV2 (ImageNet)")
                        st.write(f"- Input Size: 224x224x3")
                        st.write(f"- Animal Keywords: {len(classifier.animal_keywords)} types")
                
                # Additional actions
                st.subheader("📋 Actions")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("🔄 Try Again"):
                        st.rerun()
                
                with col_b:
                    if st.button("💾 Save Result"):
                        result_text = f"Animal: {animal_type}\nConfidence: {confidence:.2%}\nTime: {processing_time:.2f}s"
                        st.download_button(
                            "📥 Download",
                            result_text,
                            file_name="classification_result.txt",
                            mime="text/plain"
                        )
                
                with col_c:
                    if st.button("🔍 Analyze Again"):
                        # Force reload models and reprocess
                        st.cache_resource.clear()
                        st.rerun()
                        
            except Exception as e:
                st.markdown(f"""
                <div class="result-box error-box">
                    <h3>❌ Processing Error</h3>
                    <p><strong>Error:</strong> {str(e)}</p>
                    <p>Please try uploading a different image or check the image format.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if show_processing_details:
                    st.exception(e)
        
        else:
            st.markdown("""
            <div class="result-box info-box">
                <h3>👆 Upload an image to get started</h3>
                <p>Select an image file using the upload button on the left, or choose a sample image to test the classifier.</p>
                <p><strong>Tip:</strong> For best results, use clear images with animals as the main subject.</p>
            </div>
            """, unsafe_allow_html=True)

def generate_sample_image(animal_type):
    """Generate a simple colored rectangle as a sample image placeholder"""
    colors = {
        "Wolf/Dog": [101, 67, 33],     # Dark brown
        "Cat": [255, 140, 0],          # Dark orange
        "Bird": [30, 144, 255],        # Dodger blue
        "Horse": [139, 69, 19],        # Saddle brown
        "Bear": [92, 51, 23],          # Dark brown
        "Elephant": [169, 169, 169],   # Dark gray
        "No Animal": [128, 128, 128]   # Gray
    }
    
    color = colors.get(animal_type, [128, 128, 128])
    image = np.full((300, 400, 3), color, dtype=np.uint8)
    
    # Add text to the image
    text = animal_type.replace("/", " or ")
    # Calculate text size for centering
    font_scale = 0.8
    thickness = 2
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
    
    # Center the text
    x = (image.shape[1] - text_width) // 2
    y = (image.shape[0] + text_height) // 2
    
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
    cv2.putText(image, "Sample Image", (x-20, y+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    return image

if __name__ == "__main__":
    main()