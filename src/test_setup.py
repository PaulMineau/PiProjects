#!/usr/bin/env python3
"""
Test script for the animal classification app
Verifies that all modules can be imported and basic functionality works
"""

import sys
import os
import numpy as np

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test basic imports
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import OpenCV: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import NumPy: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✓ TensorFlow imported successfully")
        print(f"  TensorFlow version: {tf.__version__}")
    except ImportError as e:
        print(f"✗ Failed to import TensorFlow: {e}")
        return False
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Streamlit: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ PIL/Pillow imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PIL/Pillow: {e}")
        return False
    
    return True

def test_modules():
    """Test that our custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from utils.image_processing import preprocess_image, validate_image
        print("✓ Image processing utilities imported successfully")
        
        # Test with a dummy image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        is_valid, message = validate_image(test_image)
        print(f"  Image validation test: {is_valid}, {message}")
        
    except ImportError as e:
        print(f"✗ Failed to import image processing utilities: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing image processing: {e}")
        return False
    
    try:
        from models.model_utils import AnimalClassifier
        print("✓ Model utilities imported successfully")
        
        # Note: We won't actually load the model in the test to avoid long download times
        print("  (Model loading test skipped to avoid download time)")
        
    except ImportError as e:
        print(f"✗ Failed to import model utilities: {e}")
        return False
    except Exception as e:
        print(f"✗ Error testing model utilities: {e}")
        return False
    
    return True

def test_streamlit_app():
    """Test that the main Streamlit app can be imported"""
    print("\nTesting Streamlit app...")
    
    try:
        # Just test that the file can be imported without running it
        import animal_classifier
        print("✓ Main Streamlit app can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import Streamlit app: {e}")
        return False
    except Exception as e:
        print(f"✗ Error importing Streamlit app: {e}")
        return False

def main():
    """Run all tests"""
    print("Animal Classification App - Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test modules
    if not test_modules():
        all_passed = False
    
    # Test Streamlit app
    if not test_streamlit_app():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The app is ready to run.")
        print("\nTo start the app, run:")
        print("streamlit run animal_classifier.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\nMake sure you have installed all dependencies:")
        print("pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)