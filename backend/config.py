"""Configuration settings for the video generation backend."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BRIA_API_TOKEN = os.getenv("BRIA_API_TOKEN")
BRIA_API_URL = "https://engine.prod.bria-api.com/v2/image/generate"

# Gemini Configuration
GEMINI_MODEL = "gemini-2.0-flash"

# File paths
BASE_DIR = Path(__file__).parent.parent
AUDIO_DIR = BASE_DIR / "audio_file"
OUTPUT_DIR = BASE_DIR / "out"
VIDEO_DIR = BASE_DIR / "videos"

# Create directories
for directory in [AUDIO_DIR, OUTPUT_DIR, VIDEO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = BASE_DIR / "users.db"

# Auth
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
