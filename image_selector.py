import random
import re

class ImageSelector:
    def __init__(self):
        # Diverse image collections for different story types and scenes
        self.image_collections = {
            # Robot/Sci-fi images
            'robot': [
                'https://images.unsplash.com/photo-1485827404703-89b55fcc595e',  # Modern robot
                'https://images.unsplash.com/photo-1535378917042-10a22c95931a',  # AI concept
                'https://images.unsplash.com/photo-1531746790731-6bf18d3c3f2b',  # Futuristic tech
                'https://images.unsplash.com/photo-1485827404703-89b55fcc595e',  # Robot arm
                'https://images.unsplash.com/photo-1507146153580-69a1fe6d8aa1'   # Tech interface
            ],
            
            # Door/Mystery images
            'door': [
                'https://images.unsplash.com/photo-1509205477838-a534e43a849f',  # Old door
                'https://images.unsplash.com/photo-1527689368864-3a821dbccc34',  # Mysterious hallway
                'https://images.unsplash.com/photo-1528696892704-5e1122852276',  # Ancient portal
                'https://images.unsplash.com/photo-1572883454114-1cf0031ede2a',  # Secret entrance
                'https://images.unsplash.com/photo-1518972559570-7cc1309f3229'   # Hidden path
            ],
            
            # Adventure/Fantasy images
            'adventure': [
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4',  # Mountain vista
                'https://images.unsplash.com/photo-1472145246862-b24cf25c4a36',  # Forest path
                'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634',  # Medieval castle
                'https://images.unsplash.com/photo-1518709268805-4e9042af2176',  # Ancient ruins
                'https://images.unsplash.com/photo-1510279770292-4b34de9f5c23'   # Mystical landscape
            ],
            
            # Sci-fi images
            'scifi': [
                'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa',  # Space
                'https://images.unsplash.com/photo-1451187580459-43490279c0fa',  # Future city
                'https://images.unsplash.com/photo-1534996858221-380b92700493',  # Tech lab
                'https://images.unsplash.com/photo-1517976547714-720226b864c1',  # Cyberpunk
                'https://images.unsplash.com/photo-1516192518150-0d8fee5425e3'   # Space station
            ],
            
            # Mystery/Thriller images
            'mystery': [
                'https://images.unsplash.com/photo-1519822472072-ec86d5ab6f5c',  # Dark alley
                'https://images.unsplash.com/photo-1509205477838-a534e43a849f',  # Mysterious room
                'https://images.unsplash.com/photo-1503708928676-1cb796a0891e',  # Foggy street
                'https://images.unsplash.com/photo-1547483029-77784da27709',  # Clue scene
                'https://images.unsplash.com/photo-1504851149312-7a075b496cc7'   # Investigation
            ],
            
            # Romance images
            'romance': [
                'https://images.unsplash.com/photo-1499198116522-4a6235013d63',  # Sunset couple
                'https://images.unsplash.com/photo-1518199266791-5375a83190b7',  # Garden romance
                'https://images.unsplash.com/photo-1503614472-8c93d56e92ce',  # Romantic cafe
                'https://images.unsplash.com/photo-1511632765486-a01980e01a18',  # Love letter
                'https://images.unsplash.com/photo-1518895949257-7621c3c786d7'   # Romantic moment
            ],
            
            # Horror images
            'horror': [
                'https://images.unsplash.com/photo-1509248961158-e54f6934749c',  # Dark forest
                'https://images.unsplash.com/photo-1502136969935-8d8eef54d77b',  # Haunted house
                'https://images.unsplash.com/photo-1533749871411-5e21e14bcc7d',  # Creepy corridor
                'https://images.unsplash.com/photo-1503708928676-1cb796a0891e',  # Fog night
                'https://images.unsplash.com/photo-1518709268805-4e9042af2176'   # Abandoned building
            ],
            
            # Nature/Peaceful images
            'nature': [
                'https://images.unsplash.com/photo-1441974231531-c6227db76b6e',  # Forest
                'https://images.unsplash.com/photo-1507525428034-b723cf961d3e',  # Beach
                'https://images.unsplash.com/photo-1465146344425-f00d5f5c8f07',  # Mountain lake
                'https://images.unsplash.com/photo-1472214103451-9374bd1c798e',  # Sunrise
                'https://images.unsplash.com/photo-1469474968028-56623f02e42e'   # Landscape
            ],
            
            # Default/General images
            'default': [
                'https://images.unsplash.com/photo-1490730141103-6cac27016106',  # Peaceful sky
                'https://images.unsplash.com/photo-1501854140801-50d01698950b',  # Nature
                'https://images.unsplash.com/photo-1518895949257-7621c3c786d7',  # People
                'https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e',  # Study
                'https://images.unsplash.com/photo-1507208773393-40d9fc670acf'   # Abstract
            ]
        }
        
        # Scene-specific keywords for better matching
        self.scene_keywords = {
            'introduction': ['start', 'beginning', 'first', 'meet', 'discover', 'find'],
            'conflict': ['problem', 'danger', 'challenge', 'fight', 'struggle', 'obstacle'],
            'climax': ['peak', 'final', 'ultimate', 'showdown', 'battle', 'crisis'],
            'resolution': ['end', 'conclusion', 'solution', 'victory', 'peace', 'happy']
        }
    
    def extract_keywords(self, text):
        """Extract relevant keywords from text for image matching"""
        text_lower = text.lower()
        keywords = []
        
        # Check for story type keywords
        if any(word in text_lower for word in ['robot', 'android', 'machine', 'cyborg']):
            keywords.append('robot')
        if any(word in text_lower for word in ['door', 'gate', 'entrance', 'portal']):
            keywords.append('door')
        if any(word in text_lower for word in ['adventure', 'journey', 'quest', 'explore']):
            keywords.append('adventure')
        if any(word in text_lower for word in ['space', 'alien', 'future', 'technology']):
            keywords.append('scifi')
        if any(word in text_lower for word in ['mystery', 'secret', 'hidden', 'clue']):
            keywords.append('mystery')
        if any(word in text_lower for word in ['love', 'romance', 'heart', 'relationship']):
            keywords.append('romance')
        if any(word in text_lower for word in ['scary', 'horror', 'fear', 'dark']):
            keywords.append('horror')
            
        return keywords
    
    def get_scene_specific_image(self, image_prompt, story_genre=None, scene_type=None):
        """Get a relevant image based on the prompt, genre, and scene type"""
        try:
            # Extract keywords from the image prompt
            keywords = self.extract_keywords(image_prompt)
            
            # Determine the best image collection to use
            image_collection = 'default'
            
            # Priority: specific keywords > story genre > scene type
            if keywords:
                for keyword in keywords:
                    if keyword in self.image_collections:
                        image_collection = keyword
                        break
            
            # If no specific keywords found, try story genre
            if image_collection == 'default' and story_genre:
                genre_lower = story_genre.lower()
                if 'sci' in genre_lower or 'robot' in genre_lower:
                    image_collection = 'robot'
                elif 'mystery' in genre_lower or 'thriller' in genre_lower:
                    image_collection = 'mystery'
                elif 'adventure' in genre_lower or 'fantasy' in genre_lower:
                    image_collection = 'adventure'
                elif 'romance' in genre_lower:
                    image_collection = 'romance'
                elif 'horror' in genre_lower:
                    image_collection = 'horror'
            
            # Get images from the selected collection
            available_images = self.image_collections.get(image_collection, self.image_collections['default'])
            
            # Add some randomness to ensure variety
            random.shuffle(available_images)
            
            # Return a random image from the collection
            return random.choice(available_images)
            
        except Exception as e:
            print(f"Error in get_scene_specific_image: {e}")
            # Fallback to default image
            return random.choice(self.image_collections['default'])
    
    def get_demo_image(self):
        """Get a random demo image"""
        all_images = []
        for collection in self.image_collections.values():
            all_images.extend(collection)
        return random.choice(all_images)
