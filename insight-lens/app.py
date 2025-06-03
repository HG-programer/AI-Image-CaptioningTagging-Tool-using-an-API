from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import io # To handle image bytes in memory
import os # For saving temporary files if needed

app = Flask(__name__)

# --- Model Configuration & Loading ---
MODEL_NAME = "nlpconnect/vit-gpt2-image-captioning"
model = None
feature_extractor = None
tokenizer = None
device = None

def load_model():
    global model, feature_extractor, tokenizer, device
    try:
        print("Backend: Loading AI model and tokenizer...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)
        feature_extractor = ViTImageProcessor.from_pretrained(MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model.to(device)
        model.eval() # Set model to evaluation mode
        print(f"Backend: Model loaded successfully on {device}.")
    except Exception as e:
        print(f"Backend: CRITICAL ERROR - Failed to load AI model: {e}")
        # In a real app, you might want to prevent the app from starting
        # or have a fallback mechanism. For now, it will fail at prediction.

# Call load_model() when the Flask app starts
load_model()

def predict_caption_from_bytes(image_bytes):
    global model, feature_extractor, tokenizer, device
    if not all([model, feature_extractor, tokenizer, device]):
        raise Exception("AI Model is not loaded properly.")
    try:
        print("Backend: Predicting caption from image bytes...")
        # Open image from bytes using Pillow and BytesIO
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Preprocess the image
        pixel_values = feature_extractor(images=[image], return_tensors="pt").pixel_values.to(device)
        
        # Generate caption
        # You can adjust max_length and num_beams as needed
        # Common parameters for this model:
        gen_kwargs = {"max_length": 40}
        output_ids = model.generate(pixel_values, **gen_kwargs)
        
        # Decode the caption
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        print(f"Backend: Generated caption: {caption}")
        return caption
    except Exception as e:
        print(f"Backend: Error during caption prediction: {e}")
        raise # Re-raise the exception to be caught by the route handler

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    print("Backend: /analyze-image endpoint hit!")

    if not all([model, feature_extractor, tokenizer, device]):
        print("Backend ERROR: AI Model is not available.")
        return jsonify({'error': 'AI service is not available on the server.'}), 503

    image_file = request.files.get('imageFile')
    image_url_input = request.form.get('imageUrl')
    image_bytes_data = None # Renamed to avoid conflict with variable name

    if image_file:
        print(f"Backend: Received image file: {image_file.filename}")
        image_bytes_data = image_file.read()
    elif image_url_input:
        print(f"Backend: Received image URL: {image_url_input}")
        try:
            # Import requests here if only used in this block
            import requests 
            response = requests.get(image_url_input, stream=True, timeout=10)
            response.raise_for_status()
            image_bytes_data = response.content
            print("Backend: Successfully fetched image from URL.")
        except requests.exceptions.RequestException as e:
            print(f"Backend: Error fetching image from URL {image_url_input}: {e}")
            return jsonify({'error': f'Could not fetch image from URL: {e}'}), 400
        except NameError: # If requests wasn't imported because it's only for URL
            print("Backend: 'requests' library not available for URL fetching.")
            return jsonify({'error': 'Server cannot fetch images from URL currently.'}), 501

    else:
        print("Backend: No image file or URL received.")
        return jsonify({'error': 'No image data received'}), 400

    if not image_bytes_data:
        print("Backend: Image bytes are empty after processing input.")
        return jsonify({'error': 'Failed to process image input.'}), 500

    try:
        caption = predict_caption_from_bytes(image_bytes_data)
        return jsonify({"ai_caption": caption})
    except Exception as e:
        print(f"Backend: Error in AI prediction processing: {e}")
        # Log the full traceback for server-side debugging
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error during AI processing on server: {str(e)}'}), 500

if __name__ == '__main__':
    # IMPORTANT: For local model loading, avoid reloader in production or if model loading is slow
    # For development, debug=True is fine, but be aware it might reload the model on code changes.
    app.run(debug=True, use_reloader=False) # use_reloader=False can prevent multiple model loads during dev
