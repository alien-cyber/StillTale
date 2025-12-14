# StillTale

StillTale is an AI-powered Slideshow video generation platform that converts text prompts or full stories into complete videos with consistent characters, scene visuals, and voiceover narration.

[Watch the Demo ](https://www.youtube.com/watch?v=LgTmTHYdntY)

### How We Use Bria FIBO

1. **Character Reference Images**: When the story mentions characters like "Luna with silver hair," we call Bria's text-to-image endpoint to generate a reference portrait with Detailed description. This image is stored and reused to keep the character looking consistent.

2. **Scene Generation**: For each scene, we send a descriptive prompt to Bria. If the scene includes a known character, we pass the character's reference image using Bria's image-to-image feature, ensuring visual consistency throughout the video.



## Tech Stack

**Backend:**
- Python, FastAPI, SQLite
- Google Gemini AI (story generation, scene creation)
- Bria AI API (image generation)
- gTTS (text-to-speech)
- OpenCV, FFmpeg (video processing)

**Frontend:**
- React, Tailwind CSS
- Axios, React Router

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- FFmpeg installed and in PATH

Create a `.env` file in the root directory:

```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=project-region
GOOGLE_GENAI_USE_VERTEXAI=True
BRIA_API_TOKEN=your-bria-api-token

```

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
cp example.env .env
# Edit .env with your credentials

# Run backend
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```








