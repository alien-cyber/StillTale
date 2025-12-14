"""Gemini AI Service - Chat session and content generation."""

import re
import json
from typing import List
from google import genai

from ..config import GEMINI_MODEL

# Initialize Gemini client
gemini_client = genai.Client()


class GeminiSession:
    """Maintains a chat session with Gemini for context-aware responses."""
    
    def __init__(self):
        self.chat = None
        self.story = None
        self.characters = []
        self.scenes = []
    
    def start_session(self, story: str):
        """Start a new chat session with the story context."""
        self.story = story
        self.chat = gemini_client.chats.create(model=GEMINI_MODEL)
        
        init_prompt = f"""You are a video generation assistant. I will give you a story and ask you questions about it.
Remember all details throughout our conversation.

STORY:
{story}

Acknowledge you understand the story and are ready to help with video generation tasks."""
        
        response = self.chat.send_message(init_prompt)
        print(f"[GeminiSession] Started: {response.text[:100]}...")
        return response.text
    
    def ask(self, prompt: str) -> str:
        """Send a message in the current session."""
        if not self.chat:
            raise ValueError("Session not started. Call start_session first.")
        response = self.chat.send_message(prompt)
        return response.text
    
    def identify_characters(self) -> List[dict]:
        """Identify characters from the story."""
        prompt = """Based on the story I gave you, identify all unique characters.
For each character provide name and physical description.

Return ONLY a JSON array (no other text):
[{"name": "CharName", "description": "brief physical description"}]

If no characters, return: []"""
        
        result = self.ask(prompt)
        
        try:
            match = re.search(r'\[.*\]', result, re.DOTALL)
            if match:
                self.characters = json.loads(match.group())
                return self.characters
            return []
        except:
            print(f"[identify_characters] Failed to parse: {result}")
            return []
    
    def create_scenes(self) -> List[dict]:
        """Break story into scenes."""
        char_names = [c["name"] for c in self.characters]
        
        prompt = f"""Break the story into 3-5 scenes for video generation.
Known characters: {char_names}

For each scene provide:
- description: Short visual description (1-2 sentences)
- characters: Which characters appear (from: {char_names})
- narration: Voiceover text

Return ONLY a JSON array:
[{{"description": "...", "characters": ["..."], "narration": "..."}}]"""
        
        result = self.ask(prompt)
        
        try:
            match = re.search(r'\[.*\]', result, re.DOTALL)
            if match:
                self.scenes = json.loads(match.group())
                return self.scenes
            sentences = [s.strip() for s in self.story.split(".") if s.strip()]
            return [{"description": s, "characters": [], "narration": s} for s in sentences]
        except:
            sentences = [s.strip() for s in self.story.split(".") if s.strip()]
            return [{"description": s, "characters": [], "narration": s} for s in sentences]
    
    def get_image_prompt(self, scene_description: str) -> str:
        """Generate image prompt for a scene."""
        prompt = f"""Create a SHORT image prompt (max 2 sentences) for this scene:
"{scene_description}"

Format: [subject], [action], [setting], [style], [lighting]
Output ONLY the prompt."""
        
        return self.ask(prompt).strip()
    
    def select_character_for_scene(self, scene_description: str, available_chars: List[str]) -> str:
        """Select the most relevant character for a scene."""
        if len(available_chars) == 1:
            return available_chars[0]
        
        prompt = f"""For this scene: "{scene_description}"
Available characters: {available_chars}

Which ONE character is most prominent? Return ONLY the name."""
        
        result = self.ask(prompt).strip()
        return result if result in available_chars else available_chars[0]
    
    def close(self):
        """Close the session."""
        self.chat = None
        self.story = None
        self.characters = []
        self.scenes = []


def generate_story(context: str) -> str:
    """Generate a creative story from a prompt."""
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"""Generate a creative story of max 200 words about: {context}

Rules:
- Include 1-2 named characters with brief descriptions
- Break into clear scenes separated by periods
- Be imaginative and engaging

Output the story only."""
    )
    return response.text
