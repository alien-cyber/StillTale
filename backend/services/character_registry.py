"""Character Registry - Stores character images for consistency."""

from typing import Dict, List


class CharacterRegistry:
    """Manages character reference images for consistent appearance."""
    
    def __init__(self):
        self.characters: Dict[str, dict] = {}
    
    def store(self, name: str, image_url: str, local_path: str, description: str):
        """Store a character with its reference image URL and local path."""
        self.characters[name] = {
            "image_url": image_url,
            "local_path": local_path,
            "description": description
        }
        print(f"[CharacterRegistry] Stored character: {name}")
    
    def get_image_urls(self, names: List[str]) -> Dict[str, str]:
        """Get image URLs for given character names."""
        return {
            name: self.characters[name]["image_url"]
            for name in names if name in self.characters
        }
    
    def get_local_paths(self, names: List[str]) -> Dict[str, str]:
        """Get local paths for given character names."""
        return {
            name: self.characters[name]["local_path"]
            for name in names if name in self.characters
        }
    
    def clear(self):
        """Clear all characters."""
        self.characters.clear()
