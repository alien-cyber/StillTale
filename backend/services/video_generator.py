"""Video Generator - Main pipeline for video generation."""

import os
import time
import uuid
from typing import Callable, Optional

from ..config import VIDEO_DIR
from .character_registry import CharacterRegistry
from .gemini_service import GeminiSession, generate_story
from .bria_service import generate_character_image, text_to_image, image_to_image
from .audio_service import text_to_audio, get_audio_duration, merge_audio_files
from .video_service import images_to_video, merge_video_audio, cleanup_files


def generate_video_from_story(
    story: str, 
    video_id: str = None,
    progress_callback: Optional[Callable[[float, str], None]] = None
) -> str:
    """
    Generate video from a story.
    
    Args:
        story: The story text to generate video from
        video_id: Optional video ID (generated if not provided)
        progress_callback: Optional callback(progress: float, message: str)
    
    Returns:
        Path to the generated video file
    """
    if not video_id:
        video_id = str(uuid.uuid4())[:8]
    character_registry = CharacterRegistry()
    gemini_session = GeminiSession()
    
    def update_progress(progress: float, message: str):
        if progress_callback:
            progress_callback(progress, message)
        print(f"[Pipeline] {progress*100:.0f}% - {message}")
    
    update_progress(0.05, "Starting session...")
    print(f"\n{'='*60}")
    print(f"Starting video generation: {video_id}")
    print(f"{'='*60}\n")
    
    gemini_session.start_session(story)
    
    try:
        # Step 1: Identify characters
        update_progress(0.1, "Identifying characters...")
        characters = gemini_session.identify_characters()
        print(f"[Pipeline] Found {len(characters)} characters: {[c['name'] for c in characters]}")
        
        # Step 2: Generate character images
        if characters:
            update_progress(0.2, "Generating character images...")
            for i, char in enumerate(characters):
                try:
                    result = generate_character_image(char["name"], char["description"], video_id)
                    character_registry.store(
                        char["name"], 
                        result["url"],
                        result["local_path"],
                        char["description"]
                    )
                    update_progress(0.2 + (0.15 * (i + 1) / len(characters)), f"Generated {char['name']}")
                    time.sleep(2)
                except Exception as e:
                    print(f"[Pipeline] Failed to generate character {char['name']}: {e}")
        
        # Step 3: Create scenes
        update_progress(0.4, "Creating scenes...")
        scenes = gemini_session.create_scenes()
        print(f"[Pipeline] Created {len(scenes)} scenes")
        
        # Step 4: Process each scene
        image_list = []
        fps = 24
        
        for i, scene in enumerate(scenes):
            scene_progress = 0.4 + (0.4 * i / len(scenes))
            update_progress(scene_progress, f"Processing scene {i+1}/{len(scenes)}...")
            
            narration = scene.get("narration", scene.get("description", ""))
            text_to_audio(narration, i, video_id)
            duration = get_audio_duration(i, video_id)
            
            description = scene.get("description", narration)
            scene_characters = scene.get("characters", [])
            char_urls = character_registry.get_image_urls(scene_characters)
            
            try:
                image_prompt = gemini_session.get_image_prompt(description)
                
                if char_urls:
                    image_path = image_to_image(image_prompt, char_urls, video_id, i, gemini_session)
                else:
                    image_path = text_to_image(image_prompt, video_id, i)
                
                frame_count = round(fps * duration)
                image_list.extend([image_path] * frame_count)
                print(f"[Pipeline] Scene {i}: {frame_count} frames, duration: {duration:.2f}s")
                
            except Exception as e:
                print(f"[Pipeline] Error in scene {i}: {e}")
                continue
            
            time.sleep(2)
        
        if not image_list:
            raise ValueError("No images generated")
        
        # Step 5: Create video
        update_progress(0.85, "Creating video...")
        temp_video = str(VIDEO_DIR / f"temp_video_{video_id}.mp4")
        images_to_video(image_list, temp_video, fps)
        
        # Step 6: Merge audio
        update_progress(0.9, "Adding audio...")
        temp_audio = str(VIDEO_DIR / f"temp_audio_{video_id}.mp3")
        merge_audio_files(video_id, temp_audio)
        
        # Step 7: Final merge
        update_progress(0.95, "Finalizing...")
        final_video = str(VIDEO_DIR / f"output_{video_id}.mp4")
        merge_video_audio(temp_video, temp_audio, final_video)
        
        # Cleanup
        try:
            os.remove(temp_video)
            os.remove(temp_audio)
            cleanup_files(video_id)
        except Exception as e:
            print(f"[Pipeline] Cleanup error: {e}")
        
        update_progress(1.0, "Done!")
        print(f"\n{'='*60}")
        print(f"Video complete: {final_video}")
        print(f"{'='*60}\n")
        
        return final_video
        
    finally:
        gemini_session.close()


def generate_video_from_prompt(prompt: str, video_id: str = None, progress_callback: Optional[Callable] = None) -> str:
    """Generate video from a prompt (generates story first)."""
    if progress_callback:
        progress_callback(0, "Generating story...")
    
    story = generate_story(prompt)
    print(f"[video_from_prompt] Generated story:\n{story}\n")
    
    time.sleep(2)
    return generate_video_from_story(story, video_id, progress_callback)
