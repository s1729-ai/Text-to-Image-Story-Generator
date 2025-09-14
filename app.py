from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import uuid
import tempfile
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image
from image_selector import ImageSelector

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Create necessary directories if they don't exist
if not os.path.exists('temp_images'):
    os.makedirs('temp_images')
if not os.path.exists('static'):
    os.makedirs('static')

class StoryGenerator:
    def __init__(self):
        """Initialize story generator in demo mode"""
        self.image_selector = ImageSelector()
        print("Running in demo mode - using pre-generated stories and images")
    
    def generate_story(self, idea, genre="fantasy", tone="adventurous", audience="general", art_style="realistic"):
        """Generate a demo story (no API required)"""
        # Create a demo story based on the user's idea
        demo_story = {
            "title": f"The Tale of {idea}",
            "genre": genre,
            "theme": f"An {tone} story about {idea}",
            "scenes": [
                {
                    "scene_number": 1,
                    "title": "The Beginning",
                    "text": f"In a {genre} world, our story begins with {idea}. The atmosphere was filled with {tone} energy as the adventure was about to unfold. The {audience} audience would soon discover an incredible tale.",
                    "image_prompt": f"A {art_style} scene showing {idea} in a {genre} setting"
                },
                {
                    "scene_number": 2,
                    "title": "The Discovery",
                    "text": f"As the story progressed, new elements of {idea} came to light. Each moment brought fresh surprises and unexpected turns. The {tone} nature of the tale kept everyone engaged.",
                    "image_prompt": f"A {art_style} illustration of the discovery moment related to {idea}"
                },
                {
                    "scene_number": 3,
                    "title": "The Challenge",
                    "text": f"Suddenly, a great challenge appeared. The world of {idea} faced its greatest test yet. The {tone} atmosphere intensified as the stakes grew higher.",
                    "image_prompt": f"A dramatic {art_style} scene showing the challenge in {idea}"
                },
                {
                    "scene_number": 4,
                    "title": "The Climax",
                    "text": f"Everything came to a head in an explosive moment. The true nature of {idea} was revealed. The {audience} watched in amazement as events unfolded.",
                    "image_prompt": f"An intense {art_style} illustration of the climactic moment in {idea}"
                },
                {
                    "scene_number": 5,
                    "title": "The Resolution",
                    "text": f"Finally, everything came together. The story of {idea} reached its natural conclusion. The {tone} journey had transformed everyone involved.",
                    "image_prompt": f"A satisfying {art_style} conclusion scene for {idea}"
                }
            ]
        }
        return demo_story
        
        # Since we're running in demo mode, we'll return the demo story
        return demo_story
    
    def generate_demo_story(self, idea, genre="fantasy", tone="adventurous", audience="general", art_style="realistic"):
        """Generate a fallback demo story"""
        return {
            "title": f"A Simple Tale of {idea}",
            "genre": genre,
            "theme": f"A {tone} story",
            "scenes": [
                {
                    "scene_number": 1,
                    "title": "Once Upon a Time",
                    "text": f"In a world of {genre}, there was {idea}. The story begins to unfold.",
                    "image_prompt": f"A simple {art_style} scene of {idea}"
                },
                {
                    "scene_number": 2,
                    "title": "And Then...",
                    "text": f"Something interesting happened with {idea}, leading to new discoveries.",
                    "image_prompt": f"A {art_style} illustration of {idea} in action"
                },
                {
                    "scene_number": 3,
                    "title": "The Plot Thickens",
                    "text": f"The situation with {idea} became more complex and intriguing.",
                    "image_prompt": f"A detailed {art_style} scene focused on {idea}"
                }
            ]
        }
    
    def generate_image(self, prompt, art_style="realistic"):
        """Generate an image using demo images from Unsplash"""
        try:
            # Use the image selector to get a relevant demo image
            image_url = self.image_selector.get_scene_specific_image(prompt, "fantasy", "default")
            
            # Download and save the image locally for better performance
            try:
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    # Create unique filename
                    unique_id = str(uuid.uuid4())
                    temp_path = os.path.join('static', f"{unique_id}.jpg")
                    
                    # Save the image
                    with open(temp_path, "wb") as f:
                        f.write(img_response.content)
                    
                    # Return local path
                    return f"/static/{unique_id}.jpg"
                else:
                    print(f"Failed to download image: {img_response.status_code}")
                    return image_url  # Fall back to direct URL if download fails
            except Exception as e:
                print(f"Error saving image locally: {e}")
                return image_url  # Fall back to direct URL if save fails
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Return demo image when everything fails
            return self.get_demo_image(prompt, art_style)
    
    def get_demo_image(self, prompt, art_style="realistic"):
        """Get a demo image based on the prompt"""
        # Use the scene-specific image selection for better relevance
        return self.image_selector.get_scene_specific_image(prompt, "fantasy", "default")
    

story_generator = StoryGenerator()

@app.route('/api/generate-story', methods=['POST'])
def generate_story():
    """Generate a complete story with images"""
    try:
        data = request.json
        idea = data.get('idea', '').strip()
        genre = data.get('genre', 'fantasy')
        tone = data.get('tone', 'adventurous')
        audience = data.get('audience', 'general')
        art_style = data.get('art_style', 'realistic')
        
        if not idea:
            return jsonify({'error': 'Story idea is required'}), 400
            
        # We're always in demo mode now
        pass
        
        # Generate the story structure
        story_data = story_generator.generate_story(idea, genre, tone, audience, art_style)
        
        if not story_data or not isinstance(story_data, dict) or 'scenes' not in story_data:
            return jsonify({'error': 'Failed to generate a valid story structure'}), 500
        
        # Generate images for each scene
        for scene in story_data['scenes']:
            try:
                image_url = story_generator.generate_image(scene['image_prompt'], art_style)
                if not image_url:
                    raise ValueError("Failed to generate image")
                scene['image_url'] = image_url
            except Exception as img_error:
                print(f"Error generating image for scene {scene.get('scene_number')}: {img_error}")
                # Try one more time with a simplified prompt
                try:
                    simplified_prompt = f"Create a {art_style} style image of: {scene['title']}"
                    image_url = story_generator.generate_image(simplified_prompt, art_style)
                    scene['image_url'] = image_url if image_url else None
                except:
                    scene['image_url'] = None
        
        return jsonify(story_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/regenerate-scene', methods=['POST'])
def regenerate_scene():
    """Regenerate a specific scene or its image"""
    try:
        data = request.json
        scene_text = data.get('scene_text', '')
        image_prompt = data.get('image_prompt', '')
        art_style = data.get('art_style', 'realistic')
        regenerate_type = data.get('type', 'both')  # 'text', 'image', or 'both'
        
        result = {}
        
        if regenerate_type in ['text', 'both']:
            try:
                # Enhance the text without API - add more descriptive elements
                words = scene_text.split()
                if len(words) > 10:
                    # Add some descriptive elements and improve formatting
                    enhanced_text = scene_text.replace(".", ".\n").replace("!", "!\n")
                    # Add some creative enhancements
                    if "robot" in scene_text.lower():
                        enhanced_text = enhanced_text.replace("robot", "mechanical being")
                    if "door" in scene_text.lower():
                        enhanced_text = enhanced_text.replace("door", "mysterious portal")
                    result['new_text'] = enhanced_text
                else:
                    result['new_text'] = scene_text
            except Exception as e:
                result['new_text'] = scene_text
        
        if regenerate_type in ['image', 'both']:
            try:
                # Try to generate a new image
                image_url = story_generator.generate_image(image_prompt, art_style)
                result['new_image_url'] = image_url
            except Exception as e:
                # Fallback: Use demo image based on the prompt
                result['new_image_url'] = story_generator.get_demo_image(image_prompt, art_style)
        
        if not result:
            return jsonify({'error': 'No changes were made'}), 400
            
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in regenerate_scene: {str(e)}")
        return jsonify({
            'error': 'Failed to regenerate scene. Using fallback options.',
            'details': str(e)
        }), 500

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Export story as PDF"""
    try:
        data = request.json
        story_data = data.get('story')
        
        if not story_data:
            return jsonify({'error': 'Story data is required'}), 400
        
        # Create PDF with custom styling
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            topMargin=72,
            bottomMargin=72,
            leftMargin=72,
            rightMargin=72
        )
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=32,
            spaceAfter=30,
            alignment=1,  # Center
            textColor='#2C3E50',
            fontName='Helvetica-Bold'
        )
        
        scene_title_style = ParagraphStyle(
            'SceneTitle',
            parent=styles['Heading2'],
            fontSize=24,
            spaceBefore=30,
            spaceAfter=20,
            textColor='#34495E',
            fontName='Helvetica-Bold'
        )
        
        scene_text_style = ParagraphStyle(
            'SceneText',
            parent=styles['Normal'],
            fontSize=12,
            leading=16,
            spaceBefore=12,
            spaceAfter=12,
            textColor='#2C3E50',
            fontName='Helvetica'
        )
        
        story = []
        
        # Add cover page
        story.append(Paragraph(story_data['title'], title_style))
        story.append(Spacer(1, 40))
        
        # Add metadata
        if 'genre' in story_data:
            meta_style = ParagraphStyle(
                'MetaStyle',
                parent=styles['Normal'],
                fontSize=14,
                textColor='#7F8C8D',
                alignment=1
            )
            story.append(Paragraph(f"Genre: {story_data['genre'].title()}", meta_style))
            story.append(Spacer(1, 10))
        
        story.append(Paragraph("Generated with AI Storyteller", meta_style))
        story.append(Spacer(1, 60))
        
        # Add each scene with improved formatting
        for scene in story_data['scenes']:
            # Scene header with number and title
            scene_header = f"Scene {scene['scene_number']}: {scene['title']}"
            story.append(Paragraph(scene_header, scene_title_style))
            
            # Scene text with better formatting
            paragraphs = scene['text'].split('\n\n')
            for p in paragraphs:
                if p.strip():
                    story.append(Paragraph(p.strip(), scene_text_style))
            
            # Add image if available
            if 'image_url' in scene:
                try:
                    # Download and add the image
                    import requests
                    img_response = requests.get(scene['image_url'])
                    if img_response.status_code == 200:
                        img_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                        img_temp.write(img_response.content)
                        img_temp.close()
                        
                        # Add image with proper sizing and spacing
                        img = Image.open(img_temp.name)
                        aspect = img.height / img.width
                        img_width = 400  # Fixed width in points
                        img_height = img_width * aspect
                        
                        story.append(Spacer(1, 20))
                        story.append(RLImage(img_temp.name, width=img_width, height=img_height))
                        story.append(Spacer(1, 20))
                        
                        # Clean up
                        os.unlink(img_temp.name)
                except Exception as e:
                    print(f"Error adding image to PDF: {e}")
            
            # Add page break between scenes
            story.append(PageBreak())
        
        doc.build(story)
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"{story_data['title'].replace(' ', '_')}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question and get both text response and related image"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
            
        # Generate a simple response without API
        try:
            # Create a simple response based on the question
            question_lower = question.lower()
            
            if "robot" in question_lower:
                text_response = "Robots are fascinating mechanical beings that can perform various tasks. They represent the intersection of technology and intelligence, often serving as helpers, companions, or even protagonists in stories."
                image_prompt = "A friendly robot in a futuristic setting"
            elif "door" in question_lower:
                text_response = "Doors are portals to new possibilities. They can lead to adventure, mystery, or discovery. In stories, doors often symbolize transitions and new beginnings."
                image_prompt = "A mysterious door in an ancient setting"
            elif "story" in question_lower:
                text_response = "Stories are powerful tools for imagination and learning. They transport us to different worlds, teach us lessons, and help us understand complex ideas through narrative."
                image_prompt = "A magical storybook opening with light"
            else:
                text_response = f"That's an interesting question about '{question}'. While I'm running in demo mode, I can tell you that this topic is worth exploring further through research and creative thinking."
                image_prompt = f"A creative illustration related to {question}"
            
            # Generate image
            image_url = story_generator.generate_image(image_prompt)
            
            return jsonify({
                'answer': text_response,
                'image_url': image_url
            })
            
        except Exception as e:
            print(f"Error in ask_question: {str(e)}")
            return jsonify({
                'error': 'Failed to generate response',
                'details': str(e)
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/share', methods=['POST'])
def share_story():
    """Create a shareable link for the story"""
    try:
        data = request.json
        story_data = data.get('story')
        
        if not story_data:
            return jsonify({'error': 'Story data is required'}), 400
        
        # Generate a unique ID for the story
        import uuid
        story_id = str(uuid.uuid4())
        
        # Store the story data (in a real app, this would go to a database)
        # For now, we'll store it in memory (note: this is temporary and will be lost on server restart)
        if not hasattr(app, 'shared_stories'):
            app.shared_stories = {}
        app.shared_stories[story_id] = story_data
        
        # Create the shareable URL
        share_url = f"{request.host_url}story/{story_id}"
        
        return jsonify({
            'share_url': share_url,
            'story_id': story_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/story/<story_id>')
def view_shared_story(story_id):
    """Retrieve a shared story"""
    try:
        if not hasattr(app, 'shared_stories'):
            return jsonify({'error': 'Story not found'}), 404
            
        story_data = app.shared_stories.get(story_id)
        if not story_data:
            return jsonify({'error': 'Story not found'}), 404
            
        return jsonify(story_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-openai', methods=['GET'])
def test_openai():
    """Test demo mode functionality"""
    try:
        # Since we're in demo mode, return a success response
        return jsonify({
            'status': 'success',
            'message': 'Demo mode is working correctly - no API key required',
            'api_response': 'Demo mode active - using pre-generated content'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Demo mode error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'AI Storyteller API is running'})

@app.route('/static/<filename>')
def serve_static(filename):
    """Serve static images"""
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    