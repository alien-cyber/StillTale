# StillTale

StillTale is an AI-powered Slideshow video generation platform that converts text prompts or full stories into complete videos with consistent characters, scene visuals, and voiceover narration.

## Features

- **Two Creation Modes**: Generate from a simple prompt or write your own detailed story
- **Character Consistency**: AI identifies characters and maintains their appearance across scenes
- **Automatic Scene Generation**: Stories are intelligently broken into visual scenes
- **AI Image Generation**: Stunning visuals created using Bria AI
- **Voiceover Narration**: Text-to-speech converts narration into audio
- **Video Assembly**: Images and audio merged into polished MP4 videos

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

### Environment Variables

Create a `.env` file in the root directory:

```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=True
BRIA_API_TOKEN=your-bria-api-token
SECRET_KEY=your-secret-key
```

## Usage

1. Open http://localhost:3000
2. Register or login
3. Choose "From Prompt" or "From Story" mode
4. Enter your text and click "Generate Video"
5. View your videos in "My Videos" section

## How It Works

1. **Story Analysis**: Gemini AI analyzes your input, identifies characters, and creates scenes
2. **Character Generation**: Reference images are created for each character
3. **Scene Visualization**: Bria AI generates images for each scene using character references
4. **Audio Creation**: gTTS converts narration to speech
5. **Video Assembly**: OpenCV and FFmpeg combine everything into a final video

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register new user |
| `/auth/token` | POST | Login |
| `/auth/verify` | GET | Verify token |
| `/generate-video` | POST | Start video generation |
| `/my-videos` | GET | List all videos |
| `/public-video/{id}` | GET | Stream video file |

## License

MIT
