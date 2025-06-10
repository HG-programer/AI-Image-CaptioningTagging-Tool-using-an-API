# InsightLens - AI Image Captioning Tool

InsightLens is a simple web application that allows users to upload an image and receive an AI-generated caption for it. This project demonstrates a basic full-stack application with a Python Flask backend running a local Hugging Face Transformers model for image captioning.

## Features

*   Upload image files.
*   (Optional: if you kept URL input) Input image URLs.
*   Generates image captions using a locally hosted AI model.
*   Displays the image preview and the generated caption.

## Tech Stack

*   **Frontend:** HTML, CSS, Vanilla JavaScript
*   **Backend:** Python, Flask
*   **AI/ML:** Hugging Face Transformers library, PyTorch
    *   **Model Used:** `nlpconnect/vit-gpt2-image-captioning` (Vision Transformer Encoder + GPT2 Decoder)
*   **Image Processing:** Pillow (PIL)

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd insight-lens 
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt 
    ```
    *(You'll need to create this `requirements.txt` file - see step 3 below)*

4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

    *Note: The first time you run the application, the AI model (`nlpconnect/vit-gpt2-image-captioning`) will be downloaded from Hugging Face. This may take some time and requires an internet connection.*

## Project Structure


insight-lens/
├── app.py # Main Flask application and AI logic
├── static/
│ ├── style.css # CSS for styling
│ └── script.js # Frontend JavaScript for interactivity
├── templates/
│ └── index.html # HTML template for the web page
├── uploads/ # (Optional: if you save uploaded files temporarily)
├── venv/ # (Optional: Python virtual environment - usually in .gitignore)
└── README.md # This file
└── requirements.txt # Python dependencies
└── .gitignore # Specifies intentionally untracked files
## Notes & Future Considerations

*   The caption generation currently uses a greedy search approach due to a `NotImplementedError` encountered with beam search for the specific `transformers.models.gpt2.modeling_gpt2.GPT2LMHeadModel` used as the decoder in this `VisionEncoderDecoderModel` configuration with the current library version.
*   Caption accuracy can vary depending on the image and model limitations.
*   Potential future improvements could include:
    *   Trying different captioning models.
    *   Implementing more robust error handling.
    *   Improving the UI/UX.
    *   Exploring ways to enable beam search or other advanced sampling techniques.

## Author

*   Harshit Gupta
    HG-Programmer

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.