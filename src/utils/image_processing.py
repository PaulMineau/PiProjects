#!/usr/bin/env python3
"""
Image processing utilities for animal classification
Handles image preprocessing, resizing, and format conversion
"""

import cv2
import numpy as np
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class ImageProcessor:
    def __init__(self):
        """Initialize the image processor"""
        logging.info("✅ ImageProcessor initialized")
    
    def preprocess_image(self, image, target_size=(224, 224), enhance=True):
        """
        Enhanced preprocessing for animal classification
        
        Args:
            image: Input image (PIL Image, numpy array, or file path)
            target_size: Target size as (width, height)
            enhance: Whether to apply image enhancements
            
        Returns:
            numpy array: Preprocessed image ready for model
        """
        try:
            # Convert to numpy array if needed
            if isinstance(image, str):
                # Load from file path
                image = cv2.imread(image)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif isinstance(image, Image.Image):
                # Convert PIL Image to numpy array
                image = np.array(image)
            
            # Ensure image is RGB
            if len(image.shape) == 3 and image.shape[2] == 4:
                # Convert RGBA to RGB
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            elif len(image.shape) == 3 and image.shape[2] == 1:
                # Convert grayscale to RGB
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif len(image.shape) == 2:
                # Convert grayscale to RGB
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            
            logging.info(f"🔍 Original image shape: {image.shape}")
            
            # Apply enhancements for better animal detection
            if enhance:
                image = self.enhance_for_animals(image)
            
            # Resize image while maintaining aspect ratio
            image = self.resize_with_padding(image, target_size)
            
            # Final normalization - keep in 0-255 range for MobileNetV2 preprocessing
            image = image.astype(np.float32)
            
            logging.info(f"✅ Preprocessed image shape: {image.shape}")
            return image
            
        except Exception as e:
            logging.error(f"❌ Image preprocessing failed: {e}")
            raise
    
    def enhance_for_animals(self, image):
        """
        Apply enhancements specifically for animal detection
        
        Args:
            image: Input image as numpy array
            
        Returns:
            numpy array: Enhanced image
        """
        try:
            # 1. Improve contrast to make animal features more prominent
            image = self.improve_contrast(image)
            
            # 2. Reduce noise while preserving edges
            image = cv2.bilateralFilter(image, 9, 75, 75)
            
            # 3. Sharpen the image to enhance animal features
            image = self.sharpen_image(image)
            
            # 4. Color enhancement for better feature detection
            image = self.enhance_colors(image)
            
            return image
            
        except Exception as e:
            logging.error(f"❌ Animal enhancement failed: {e}")
            return image
    
    def improve_contrast(self, image, clip_limit=2.0):
        """
        Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        """
        try:
            # Convert to LAB color space
            lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            
            # Convert back to RGB
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            return enhanced
            
        except Exception as e:
            logging.error(f"❌ Contrast improvement failed: {e}")
            return image
    
    def sharpen_image(self, image, strength=0.5):
        """
        Apply unsharp masking for better edge definition
        """
        try:
            # Create gaussian blur
            gaussian = cv2.GaussianBlur(image, (5, 5), 1.0)
            
            # Create unsharp mask
            unsharp_mask = cv2.addWeighted(image, 1.0 + strength, gaussian, -strength, 0)
            
            # Ensure values stay in valid range
            unsharp_mask = np.clip(unsharp_mask, 0, 255)
            
            return unsharp_mask.astype(np.uint8)
            
        except Exception as e:
            logging.error(f"❌ Image sharpening failed: {e}")
            return image
    
    def enhance_colors(self, image, saturation_factor=1.2):
        """
        Enhance color saturation for better animal feature detection
        """
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
            
            # Enhance saturation
            hsv[:, :, 1] = hsv[:, :, 1] * saturation_factor
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            
            # Convert back to RGB
            enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
            return enhanced
            
        except Exception as e:
            logging.error(f"❌ Color enhancement failed: {e}")
            return image
    
    def resize_with_padding(self, image, target_size, fill_color=(114, 114, 114)):
        """
        Resize image to target size while maintaining aspect ratio using padding
        
        Args:
            image: Input image as numpy array
            target_size: Target size as (width, height)
            fill_color: Color for padding (RGB tuple) - using gray instead of black
            
        Returns:
            numpy array: Resized image with padding
        """
        target_width, target_height = target_size
        height, width = image.shape[:2]
        
        # Calculate scaling factor to fit image in target size
        scale = min(target_width / width, target_height / height)
        
        # Calculate new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize image with high-quality interpolation
        if scale < 1:
            # Downscaling - use INTER_AREA for better quality
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        else:
            # Upscaling - use INTER_CUBIC for better quality
            resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Create new image with target size and fill color
        new_image = np.full((target_height, target_width, 3), fill_color, dtype=image.dtype)
        
        # Calculate padding to center the image
        y_offset = (target_height - new_height) // 2
        x_offset = (target_width - new_width) // 2
        
        # Place resized image in center
        new_image[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized
        
        return new_image
    
    def detect_and_crop_main_subject(self, image, margin=0.1):
        """
        Detect and crop the main subject (animal) in the image
        
        Args:
            image: Input image as numpy array
            margin: Additional margin around detected subject (as fraction)
            
        Returns:
            numpy array: Cropped image focused on main subject
        """
        try:
            # Convert to grayscale for processing
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Use adaptive threshold for better edge detection
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                         cv2.THRESH_BINARY, 11, 2)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (assumed to be main subject)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Add margin around the subject
                margin_x = int(w * margin)
                margin_y = int(h * margin)
                
                x = max(0, x - margin_x)
                y = max(0, y - margin_y)
                w = min(image.shape[1] - x, w + 2 * margin_x)
                h = min(image.shape[0] - y, h + 2 * margin_y)
                
                # Crop the image
                cropped = image[y:y+h, x:x+w]
                
                # Only return cropped if it's a reasonable size (at least 25% of original)
                if cropped.shape[0] * cropped.shape[1] > 0.25 * image.shape[0] * image.shape[1]:
                    logging.info(f"🔍 Cropped to main subject: {cropped.shape}")
                    return cropped
            
            # Return original if cropping didn't work well
            logging.info("🔍 No suitable crop found, using original image")
            return image
            
        except Exception as e:
            logging.error(f"❌ Subject detection failed: {e}")
            return image
    
    def get_image_info(self, image):
        """
        Get comprehensive information about the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            dict: Image information
        """
        try:
            # Basic info
            info = {
                'shape': image.shape,
                'dtype': str(image.dtype),
                'size_bytes': image.nbytes,
                'size_kb': image.nbytes / 1024,
                'channels': image.shape[2] if len(image.shape) > 2 else 1,
                'width': image.shape[1],
                'height': image.shape[0]
            }
            
            # Color analysis
            if len(image.shape) == 3:
                info['mean_rgb'] = [float(np.mean(image[:, :, i])) for i in range(3)]
                info['std_rgb'] = [float(np.std(image[:, :, i])) for i in range(3)]
                
                # Brightness and contrast metrics
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                info['brightness'] = float(np.mean(gray))
                info['contrast'] = float(np.std(gray))
                
                # Color distribution
                info['is_grayscale'] = np.allclose(image[:, :, 0], image[:, :, 1]) and np.allclose(image[:, :, 1], image[:, :, 2])
            
            return info
            
        except Exception as e:
            logging.error(f"❌ Failed to get image info: {e}")
            return {}

# Standalone functions for backward compatibility
def preprocess_image(image, target_size=(224, 224)):
    """Standalone function for image preprocessing"""
    processor = ImageProcessor()
    return processor.preprocess_image(image, target_size, enhance=True)

def resize_image(image, target_size):
    """Standalone function for image resizing"""
    processor = ImageProcessor()
    return processor.resize_with_padding(image, target_size)