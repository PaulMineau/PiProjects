#!/usr/bin/env python3
"""
Model utilities for animal classification
Uses a pre-trained MobileNetV2 model for lightweight inference suitable for Raspberry Pi
"""

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnimalClassifier:
    """Animal classification using pre-trained MobileNetV2 model"""
    
    def __init__(self):
        """Initialize the classifier with pre-trained model"""
        self.model = None
        self.input_shape = (224, 224, 3)
        self.animal_classes = self._get_animal_classes()
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained MobileNetV2 model"""
        try:
            logger.info("Loading MobileNetV2 model...")
            self.model = MobileNetV2(
                weights='imagenet',
                include_top=True,
                input_shape=self.input_shape
            )
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise e
    
    def _get_animal_classes(self):
        """Define the animal classes we can detect from ImageNet"""
        # ImageNet classes that correspond to animals
        # This is a subset of ImageNet classes mapped to common animal names
        return {
            # Dogs
            'beagle': 'Dog',
            'golden_retriever': 'Dog',
            'German_shepherd': 'Dog',
            'collie': 'Dog',
            'border_collie': 'Dog',
            'Afghan_hound': 'Dog',
            'basset': 'Dog',
            'bloodhound': 'Dog',
            'bluetick': 'Dog',
            'borzoi': 'Dog',
            'boxer': 'Dog',
            'briard': 'Dog',
            'bull_mastiff': 'Dog',
            'cairn': 'Dog',
            'Chihuahua': 'Dog',
            'chow': 'Dog',
            'clumber': 'Dog',
            'cocker_spaniel': 'Dog',
            'dachshund': 'Dog',
            'Dalmatian': 'Dog',
            'Doberman': 'Dog',
            'English_foxhound': 'Dog',
            'English_setter': 'Dog',
            'English_springer': 'Dog',
            'EntleBucher': 'Dog',
            'Eskimo_dog': 'Dog',
            'French_bulldog': 'Dog',
            
            # Cats
            'tabby': 'Cat',
            'tiger_cat': 'Cat',
            'Persian_cat': 'Cat',
            'Siamese_cat': 'Cat',
            'Egyptian_cat': 'Cat',
            
            # Wild cats
            'tiger': 'Tiger',
            'lion': 'Lion',
            'leopard': 'Leopard',
            'cheetah': 'Cheetah',
            'jaguar': 'Jaguar',
            'lynx': 'Lynx',
            
            # Birds
            'robin': 'Bird',
            'jay': 'Bird',
            'magpie': 'Bird',
            'chickadee': 'Bird',
            'water_ouzel': 'Bird',
            'kite': 'Bird',
            'bald_eagle': 'Eagle',
            'vulture': 'Bird',
            'great_grey_owl': 'Owl',
            'peacock': 'Bird',
            'lorikeet': 'Bird',
            'hummingbird': 'Bird',
            'pelican': 'Bird',
            'flamingo': 'Bird',
            'duck': 'Duck',
            'goose': 'Bird',
            'swan': 'Bird',
            'penguin': 'Penguin',
            
            # Farm animals
            'ox': 'Cow',
            'water_buffalo': 'Buffalo',
            'bison': 'Bison',
            'ram': 'Sheep',
            'bighorn': 'Sheep',
            'ibex': 'Goat',
            'hartebeest': 'Antelope',
            'impala': 'Antelope',
            'gazelle': 'Gazelle',
            
            # Horses
            'sorrel': 'Horse',
            'Arabian_horse': 'Horse',
            
            # Large mammals
            'elephant': 'Elephant',
            'Indian_elephant': 'Elephant',
            'African_elephant': 'Elephant',
            'lesser_panda': 'Panda',
            'giant_panda': 'Panda',
            'brown_bear': 'Bear',
            'American_black_bear': 'Bear',
            'ice_bear': 'Polar Bear',
            
            # Other animals
            'zebra': 'Zebra',
            'giraffe': 'Giraffe',
            'hippopotamus': 'Hippopotamus',
            'rhinoceros': 'Rhinoceros',
            'wombat': 'Wombat',
            'koala': 'Koala',
            'sloth': 'Sloth',
            'orangutan': 'Orangutan',
            'gorilla': 'Gorilla',
            'chimpanzee': 'Chimpanzee',
            'gibbon': 'Gibbon',
            'proboscis_monkey': 'Monkey',
            'macaque': 'Monkey',
            'baboon': 'Baboon',
            'capuchin': 'Monkey',
            'squirrel_monkey': 'Monkey',
            
            # Marine animals
            'killer_whale': 'Whale',
            'dugong': 'Dugong',
            'sea_lion': 'Sea Lion',
            'chihuahua': 'Dog',
        }
    
    def classify(self, image):
        """
        Classify an animal in the given image
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            dict: Classification result with animal name, confidence, and all predictions
        """
        try:
            # Preprocess the image
            processed_image = self._preprocess_for_model(image)
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Decode ImageNet predictions
            decoded_predictions = decode_predictions(predictions, top=10)[0]
            
            # Find the best animal match
            best_animal = "No Animal"
            best_confidence = 0.0
            all_predictions = []
            
            for imagenet_class, class_name, confidence in decoded_predictions:
                # Check if this ImageNet class corresponds to an animal
                animal_name = self.animal_classes.get(imagenet_class, None)
                
                if animal_name:
                    all_predictions.append((animal_name, confidence))
                    if confidence > best_confidence:
                        best_animal = animal_name
                        best_confidence = confidence
            
            # If no animal found with high confidence, check if there are any animals in top predictions
            if best_confidence < 0.1:
                for imagenet_class, class_name, confidence in decoded_predictions:
                    animal_name = self.animal_classes.get(imagenet_class, None)
                    if animal_name and confidence > best_confidence:
                        best_animal = animal_name
                        best_confidence = confidence
            
            return {
                'animal': best_animal,
                'confidence': best_confidence,
                'all_predictions': all_predictions[:5],  # Top 5 animal predictions
                'raw_predictions': decoded_predictions[:5]  # Top 5 raw ImageNet predictions
            }
            
        except Exception as e:
            logger.error(f"Error during classification: {e}")
            return {
                'animal': "Error",
                'confidence': 0.0,
                'all_predictions': [],
                'raw_predictions': []
            }
    
    def _preprocess_for_model(self, image):
        """
        Preprocess image for MobileNetV2 model
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Preprocessed image ready for model
        """
        # Resize to model input size
        resized = cv2.resize(image, (224, 224))
        
        # Convert BGR to RGB if needed
        if len(resized.shape) == 3 and resized.shape[2] == 3:
            # OpenCV uses BGR, but model expects RGB
            resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        # Add batch dimension
        resized = np.expand_dims(resized, axis=0)
        
        # Preprocess for MobileNetV2
        preprocessed = preprocess_input(resized)
        
        return preprocessed
    
    def get_input_shape(self):
        """Get the expected input shape for the model"""
        return self.input_shape
    
    def get_supported_animals(self):
        """Get list of supported animal types"""
        return list(set(self.animal_classes.values()))


def load_model():
    """Convenience function to load the classifier"""
    return AnimalClassifier()


if __name__ == "__main__":
    # Test the classifier
    classifier = AnimalClassifier()
    print("Classifier loaded successfully!")
    print(f"Input shape: {classifier.get_input_shape()}")
    print(f"Supported animals: {classifier.get_supported_animals()}")