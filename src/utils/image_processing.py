#!/usr/bin/env python3
"""
Image processing utilities for animal classification
Handles image preprocessing, resizing, and format conversion
"""

import cv2
import numpy as np
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def preprocess_image(image_input, target_size=(224, 224)):
    """
    Preprocess an image for classification
    
    Args:
        image_input: Input image (numpy array, PIL Image, or file path)
        target_size: Target size for resizing (width, height)
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    try:
        # Convert input to numpy array
        if isinstance(image_input, str):
            # File path
            image = cv2.imread(image_input)
            if image is None:
                raise ValueError(f"Could not load image from path: {image_input}")
        elif isinstance(image_input, Image.Image):
            # PIL Image
            image = np.array(image_input)
            # Convert RGB to BGR for OpenCV
            if len(image.shape) == 3 and image.shape[2] == 3:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        elif isinstance(image_input, np.ndarray):
            # Already a numpy array
            image = image_input.copy()
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")
        
        # Ensure image is in the right format
        if len(image.shape) == 2:
            # Grayscale to BGR
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif len(image.shape) == 3 and image.shape[2] == 4:
            # RGBA to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        
        # Resize image
        if target_size:
            image = resize_image(image, target_size)
        
        # Normalize pixel values to 0-255 range
        image = np.clip(image, 0, 255).astype(np.uint8)
        
        return image
        
    except Exception as e:
        logger.error("Error preprocessing image: %s", str(e))
        raise e


def resize_image(image, target_size, maintain_aspect_ratio=True):
    """
    Resize an image to target size
    
    Args:
        image (numpy.ndarray): Input image
        target_size (tuple): Target size (width, height)
        maintain_aspect_ratio (bool): Whether to maintain aspect ratio
        
    Returns:
        numpy.ndarray: Resized image
    """
    try:
        height, width = image.shape[:2]
        target_width, target_height = target_size
        
        if maintain_aspect_ratio:
            # Calculate aspect ratio
            aspect_ratio = width / height
            target_aspect_ratio = target_width / target_height
            
            if aspect_ratio > target_aspect_ratio:
                # Image is wider than target
                new_width = target_width
                new_height = int(target_width / aspect_ratio)
            else:
                # Image is taller than target
                new_height = target_height
                new_width = int(target_height * aspect_ratio)
            
            # Resize image
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # Create a blank canvas with target size
            canvas = np.zeros((target_height, target_width, 3), dtype=np.uint8)
            
            # Calculate padding
            y_offset = (target_height - new_height) // 2
            x_offset = (target_width - new_width) // 2
            
            # Place resized image on canvas
            canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
            
            return canvas
        else:
            # Direct resize without maintaining aspect ratio
            return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)
            
    except Exception as e:
        logger.error("Error resizing image: %s", str(e))
        raise e


def enhance_image(image, enhance_contrast=True, enhance_brightness=False):
    """
    Enhance image quality for better classification
    
    Args:
        image (numpy.ndarray): Input image
        enhance_contrast (bool): Whether to enhance contrast
        enhance_brightness (bool): Whether to enhance brightness
        
    Returns:
        numpy.ndarray: Enhanced image
    """
    try:
        enhanced = image.copy()
        
        if enhance_contrast:
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            l_channel, a_channel, b_channel = cv2.split(lab)
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l_channel = clahe.apply(l_channel)
            
            enhanced = cv2.merge((l_channel, a_channel, b_channel))
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        if enhance_brightness:
            # Adjust brightness
            hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            # Increase value (brightness) channel slightly
            v = cv2.add(v, 10)
            v = np.clip(v, 0, 255)
            
            enhanced = cv2.merge((h, s, v))
            enhanced = cv2.cvtColor(enhanced, cv2.COLOR_HSV2BGR)
        
        return enhanced
        
    except Exception as e:
        logger.error("Error enhancing image: %s", str(e))
        return image  # Return original image if enhancement fails


def detect_and_crop_main_object(image, padding=0.1):
    """
    Detect the main object in the image and crop around it
    
    Args:
        image (numpy.ndarray): Input image
        padding (float): Padding around detected object (0.0 to 1.0)
        
    Returns:
        numpy.ndarray: Cropped image
    """
    try:
        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply threshold
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Add padding
            height, width = image.shape[:2]
            pad_x = int(w * padding)
            pad_y = int(h * padding)
            
            x = max(0, x - pad_x)
            y = max(0, y - pad_y)
            w = min(width - x, w + 2 * pad_x)
            h = min(height - y, h + 2 * pad_y)
            
            # Crop image
            cropped = image[y:y+h, x:x+w]
            
            # Only return cropped image if it's significantly smaller than original
            crop_ratio = (w * h) / (width * height)
            if crop_ratio < 0.8:  # If cropped area is less than 80% of original
                return cropped
        
        # Return original image if cropping doesn't help
        return image
        
    except Exception as e:
        logger.error("Error detecting and cropping main object: %s", str(e))
        return image  # Return original image if detection fails


def convert_image_format(image, target_format='RGB'):
    """
    Convert image between different color formats
    
    Args:
        image (numpy.ndarray): Input image
        target_format (str): Target format ('RGB', 'BGR', 'GRAY')
        
    Returns:
        numpy.ndarray: Converted image
    """
    try:
        if len(image.shape) == 2:
            # Grayscale image
            if target_format == 'RGB':
                return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif target_format == 'BGR':
                return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            else:
                return image
        
        elif len(image.shape) == 3:
            # Color image
            if image.shape[2] == 3:
                # Assume it's BGR (OpenCV default)
                if target_format == 'RGB':
                    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                elif target_format == 'GRAY':
                    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                else:
                    return image
            elif image.shape[2] == 4:
                # RGBA image
                if target_format == 'RGB':
                    return cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                elif target_format == 'BGR':
                    return cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
                elif target_format == 'GRAY':
                    return cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
                else:
                    return image
        
        return image
        
    except Exception as e:
        logger.error("Error converting image format: %s", str(e))
        return image


def validate_image(image):
    """
    Validate that the image is suitable for processing
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        if image is None:
            return False, "Image is None"
        
        if not isinstance(image, np.ndarray):
            return False, f"Image must be numpy array, got {type(image)}"
        
        if len(image.shape) < 2 or len(image.shape) > 3:
            return False, f"Image must have 2 or 3 dimensions, got {len(image.shape)}"
        
        if image.shape[0] < 10 or image.shape[1] < 10:
            return False, f"Image too small: {image.shape[:2]}"
        
        if len(image.shape) == 3 and image.shape[2] not in [1, 3, 4]:
            return False, f"Image must have 1, 3, or 4 channels, got {image.shape[2]}"
        
        return True, "Valid image"
        
    except Exception as e:
        return False, f"Error validating image: {str(e)}"


if __name__ == "__main__":
    # Test the image processing functions
    print("Image processing utilities loaded successfully!")
    
    # Create a test image
    test_image = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    
    # Test validation
    is_valid, message = validate_image(test_image)
    print(f"Test image validation: {is_valid}, {message}")
    
    # Test preprocessing
    processed = preprocess_image(test_image)
    print(f"Preprocessed image shape: {processed.shape}")