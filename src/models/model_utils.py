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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AnimalClassifier:
    def __init__(self):
        """Initialize the animal classifier with pre-trained MobileNetV2"""
        try:
            # Load pre-trained MobileNetV2
            self.model = MobileNetV2(weights='imagenet', include_top=True)
            
            # Comprehensive animal keywords for better detection
            self.animal_keywords = [
                # Canines (dogs, wolves, foxes) - ENHANCED for wolf detection
                'dog', 'puppy', 'wolf', 'timber_wolf', 'white_wolf', 'red_wolf', 'gray_wolf', 'grey_wolf',
                'fox', 'red_fox', 'arctic_fox', 'kit_fox', 'fennec_fox', 'silver_fox',
                'coyote', 'jackal', 'dingo', 'wild_dog', 'african_wild_dog',
                'hunting_dog', 'hound', 'bloodhound', 'retriever', 'shepherd', 'terrier', 'bulldog',
                'beagle', 'poodle', 'husky', 'malamute', 'chihuahua', 'labrador',
                
                # Felines (cats, big cats)
                'cat', 'kitten', 'tabby', 'persian_cat', 'siamese_cat', 'maine_coon',
                'tiger', 'bengal_tiger', 'siberian_tiger', 'lion', 'african_lion', 'mountain_lion',
                'leopard', 'snow_leopard', 'cheetah', 'jaguar', 'lynx', 'bobcat', 'cougar', 'puma',
                'ocelot', 'serval', 'caracal', 'wildcat',
                
                # Bears
                'bear', 'brown_bear', 'black_bear', 'polar_bear', 'grizzly', 'kodiak_bear',
                'panda', 'giant_panda', 'sun_bear', 'sloth_bear',
                
                # Large mammals
                'elephant', 'african_elephant', 'indian_elephant', 'asian_elephant',
                'rhino', 'rhinoceros', 'white_rhino', 'black_rhino',
                'hippo', 'hippopotamus', 'giraffe', 'okapi',
                'zebra', 'plains_zebra', 'mountain_zebra',
                'horse', 'stallion', 'mare', 'pony', 'donkey', 'mule', 'ass',
                'cow', 'bull', 'ox', 'cattle', 'buffalo', 'bison', 'yak', 'water_buffalo',
                'sheep', 'lamb', 'ram', 'goat', 'pig', 'hog', 'boar', 'wild_boar',
                
                # Deer and related
                'deer', 'white_tailed_deer', 'mule_deer', 'elk', 'moose', 'reindeer', 'caribou',
                'antelope', 'gazelle', 'impala', 'springbok', 'chamois', 'ibex',
                
                # Primates
                'monkey', 'ape', 'gorilla', 'chimpanzee', 'orangutan', 'baboon', 'mandrill',
                'lemur', 'macaque', 'vervet', 'howler_monkey', 'spider_monkey',
                
                # Marine mammals
                'whale', 'blue_whale', 'humpback_whale', 'killer_whale', 'orca', 'sperm_whale',
                'dolphin', 'bottlenose_dolphin', 'porpoise', 'narwhal', 'beluga',
                'seal', 'harbor_seal', 'elephant_seal', 'sea_lion', 'fur_seal',
                'walrus', 'manatee', 'dugong', 'otter', 'sea_otter',
                
                # Birds
                'bird', 'eagle', 'bald_eagle', 'golden_eagle', 'hawk', 'falcon', 'kestrel',
                'owl', 'barn_owl', 'great_horned_owl', 'snowy_owl',
                'duck', 'mallard', 'canvasback', 'goose', 'canada_goose', 'swan', 'pelican',
                'chicken', 'rooster', 'hen', 'turkey', 'peacock', 'pheasant', 'quail',
                'penguin', 'emperor_penguin', 'king_penguin', 'ostrich', 'emu', 'cassowary',
                'parrot', 'macaw', 'cockatoo', 'parakeet', 'canary', 'finch',
                'robin', 'sparrow', 'cardinal', 'blue_jay', 'crow', 'raven', 'magpie',
                'hummingbird', 'woodpecker', 'flamingo', 'stork', 'crane', 'heron',
                
                # Reptiles and amphibians
                'snake', 'python', 'boa', 'cobra', 'viper', 'rattlesnake', 'garter_snake',
                'lizard', 'iguana', 'gecko', 'chameleon', 'monitor_lizard', 'komodo_dragon',
                'turtle', 'sea_turtle', 'tortoise', 'terrapin',
                'frog', 'tree_frog', 'poison_frog', 'bullfrog', 'toad', 'salamander', 'newt',
                'crocodile', 'alligator', 'caiman', 'gharial',
                
                # Small mammals
                'rabbit', 'bunny', 'hare', 'jackrabbit', 'cottontail',
                'squirrel', 'grey_squirrel', 'red_squirrel', 'flying_squirrel', 'chipmunk',
                'mouse', 'rat', 'hamster', 'gerbil', 'guinea_pig', 'chinchilla',
                'ferret', 'weasel', 'mink', 'otter', 'badger', 'skunk', 'raccoon',
                'hedgehog', 'porcupine', 'armadillo', 'anteater', 'sloth',
                'bat', 'vampire_bat', 'fruit_bat',
                
                # Marsupials
                'kangaroo', 'wallaby', 'koala', 'opossum', 'tasmanian_devil', 'wombat',
                
                # Insects and arthropods
                'butterfly', 'monarch_butterfly', 'moth', 'bee', 'honeybee', 'bumblebee',
                'wasp', 'hornet', 'ant', 'termite', 'beetle', 'ladybug', 'firefly',
                'spider', 'black_widow', 'tarantula', 'scorpion', 'tick', 'mite',
                'dragonfly', 'damselfly', 'grasshopper', 'cricket', 'katydid', 'mantis',
                'cockroach', 'fly', 'mosquito', 'gnat',
                
                # Fish and aquatic
                'fish', 'salmon', 'trout', 'bass', 'tuna', 'shark', 'great_white_shark',
                'hammerhead_shark', 'tiger_shark', 'whale_shark', 'ray', 'stingray', 'manta_ray',
                'goldfish', 'koi', 'carp', 'catfish', 'pike', 'perch', 'cod', 'halibut',
                'seahorse', 'starfish', 'jellyfish', 'octopus', 'squid', 'cuttlefish',
                'lobster', 'crab', 'shrimp', 'crayfish'
            ]
            
            logging.info(f"✅ AnimalClassifier initialized with {len(self.animal_keywords)} animal types")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize AnimalClassifier: {e}")
            raise

    def predict(self, image, top_k=5):
        """
        Get predictions from the model
        
        Args:
            image: Preprocessed image array (224, 224, 3)
            top_k: Number of top predictions to return
            
        Returns:
            list: List of (class_name, confidence) tuples
        """
        try:
            # Ensure image is the right shape and add batch dimension
            if len(image.shape) == 3:
                image = np.expand_dims(image, axis=0)
            
            # Preprocess for MobileNetV2
            processed_image = preprocess_input(image)
            
            # Get predictions
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Decode predictions
            decoded_predictions = decode_predictions(predictions, top=top_k)[0]
            
            # Format as (class_name, confidence) tuples
            formatted_predictions = [(class_name, confidence) for (_, class_name, confidence) in decoded_predictions]
            
            return formatted_predictions
            
        except Exception as e:
            logging.error(f"❌ Prediction failed: {e}")
            return []

    def classify_animal(self, image, confidence_threshold=0.1):
        """
        Classify if image contains an animal and what type
        
        Args:
            image: Preprocessed image array
            confidence_threshold: Minimum confidence for classification
            
        Returns:
            tuple: (is_animal, animal_type, confidence)
        """
        try:
            predictions = self.predict(image, top_k=10)  # Get more predictions for better animal detection
            
            if not predictions:
                return False, "Unknown", 0.0
            
            # Check all predictions for animal matches (not just the top one)
            best_animal_match = None
            best_animal_confidence = 0.0
            
            for class_name, confidence in predictions:
                # More flexible matching for animal detection
                class_lower = class_name.lower().replace('-', '_').replace(' ', '_')
                
                # Check if any animal keyword matches
                for animal_keyword in self.animal_keywords:
                    if (self._is_animal_match(animal_keyword, class_lower) and 
                        confidence > best_animal_confidence):
                        best_animal_match = class_name
                        best_animal_confidence = confidence
                        break
            
            if best_animal_match and best_animal_confidence >= confidence_threshold:
                return True, best_animal_match, best_animal_confidence
            else:
                # Return the top prediction even if not identified as animal
                top_class, top_confidence = predictions[0]
                
                # Check if top prediction might still be an animal with fuzzy matching
                top_class_lower = top_class.lower().replace('-', '_').replace(' ', '_')
                for animal_keyword in self.animal_keywords:
                    if self._fuzzy_match(animal_keyword, top_class_lower):
                        return True, top_class, top_confidence
                
                return False, top_class, top_confidence
                
        except Exception as e:
            logging.error(f"❌ Animal classification failed: {e}")
            return False, "Error", 0.0
    
    def _is_animal_match(self, keyword, class_name):
        """Check if a keyword matches a class name (exact or partial)"""
        # Exact match
        if keyword == class_name:
            return True
        
        # Keyword is contained in class name
        if keyword in class_name:
            return True
        
        # Class name is contained in keyword (for compound names)
        if class_name in keyword:
            return True
        
        # Special cases for common variations
        variations = {
            'wolf': ['timber_wolf', 'gray_wolf', 'grey_wolf', 'red_wolf', 'white_wolf'],
            'dog': ['hunting_dog', 'wild_dog'],
            'cat': ['persian_cat', 'siamese_cat'],
            'bear': ['brown_bear', 'black_bear', 'polar_bear'],
            'elephant': ['african_elephant', 'indian_elephant', 'asian_elephant']
        }
        
        for base_word, variants in variations.items():
            if keyword == base_word and any(variant in class_name for variant in variants):
                return True
            if class_name == base_word and any(variant == keyword for variant in variants):
                return True
        
        return False
    
    def _fuzzy_match(self, keyword, class_name, threshold=0.6):
        """Simple fuzzy matching for animal names"""
        if len(keyword) < 3 or len(class_name) < 3:
            return False
        
        # Check for partial matches
        if keyword in class_name or class_name in keyword:
            return True
        
        # Check for similar patterns (simple approach)
        common_chars = sum(1 for c in keyword if c in class_name)
        similarity = common_chars / max(len(keyword), len(class_name))
        
        return similarity >= threshold

    def get_input_shape(self):
        """Return the expected input shape for the model"""
        return (224, 224, 3)
    
    def get_supported_animals(self):
        """Return list of supported animal types"""
        return self.animal_keywords.copy()


def load_model():
    """Convenience function to load the classifier"""
    return AnimalClassifier()


if __name__ == "__main__":
    # Test the classifier
    classifier = AnimalClassifier()
    print("Classifier loaded successfully!")
    print(f"Input shape: {classifier.get_input_shape()}")
    print(f"Supported animals: {classifier.get_supported_animals()}")