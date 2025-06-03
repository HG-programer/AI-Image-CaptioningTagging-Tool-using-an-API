document.addEventListener('DOMContentLoaded', () => {
    const imageUploadInput = document.getElementById('imageUpload');
    const imageUrlInput = document.getElementById('imageUrl');
    const analyzeButton = document.getElementById('analyzeButton');
    const imagePreview = document.getElementById('imagePreview');
    const previewMessage = document.getElementById('previewMessage');
    const resultsContent = document.getElementById('resultsContent');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');

    // Function to display image preview
    function displayPreview(fileOrUrl) {
        previewMessage.style.display = 'none';
        imagePreview.style.display = 'block';
        if (typeof fileOrUrl === 'string') { // It's a URL
            imagePreview.src = fileOrUrl;
        } else { // It's a File object
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
            }
            reader.readAsDataURL(fileOrUrl);
        }
    }

    imageUploadInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            displayPreview(file);
            imageUrlInput.value = ''; // Clear URL input if file is chosen
        }
    });

    imageUrlInput.addEventListener('input', function(event) {
        const url = event.target.value;
        if (url) {
            // Basic check for image URL (can be improved)
            if (/\.(jpeg|jpg|gif|png)$/i.test(url)) {
                displayPreview(url);
                imageUploadInput.value = ''; // Clear file input if URL is typed
            } else {
                imagePreview.style.display = 'none';
                previewMessage.textContent = 'Please enter a valid image URL.';
                previewMessage.style.display = 'block';
            }
        }
    });


    analyzeButton.addEventListener('click', async () => {
        resultsContent.innerHTML = ''; // Clear previous results
        errorMessage.style.display = 'none'; // Hide previous error
        loadingIndicator.style.display = 'block'; // Show loading

        const formData = new FormData();
        const imageFile = imageUploadInput.files[0];
        const imageUrl = imageUrlInput.value;

        if (imageFile) {
            formData.append('imageFile', imageFile);
        } else if (imageUrl) {
            formData.append('imageUrl', imageUrl);
        } else {
            errorMessage.textContent = 'Please upload an image or provide an image URL.';
            errorMessage.style.display = 'block';
            loadingIndicator.style.display = 'none';
            return;
        }

        console.log("Frontend: Sending data to backend...");

        try {
            const response = await fetch('/analyze-image', {
                method: 'POST',
                body: formData // FormData handles content type for file uploads
            });

            loadingIndicator.style.display = 'none'; // Hide loading

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Unknown error from server' }));
                throw new Error(`Server error: ${response.status} ${response.statusText}. ${errorData.detail || errorData.error || ''}`);
            }

            const data = await response.json();
            console.log("Frontend: Received data from backend:", data);

            // Display the dummy AI response for now
            if (data.ai_caption) {
                resultsContent.innerHTML = `<p><strong>Caption:</strong> ${data.ai_caption}</p>`;
            } else if (data.message) {
                 resultsContent.innerHTML = `<p>${data.message}</p>`;
            }
            if (data.received_filename) {
                resultsContent.innerHTML += `<p><em>Backend confirmed receiving file: ${data.received_filename}</em></p>`;
            }
            if (data.received_url) {
                resultsContent.innerHTML += `<p><em>Backend confirmed receiving URL: ${data.received_url}</em></p>`;
            }


        } catch (error) {
            loadingIndicator.style.display = 'none'; // Hide loading
            console.error("Frontend: Error:", error);
            errorMessage.textContent = `Error: ${error.message}`;
            errorMessage.style.display = 'block';
        }
    });
});