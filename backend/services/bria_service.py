"""Bria API Service - Image generation."""

import base64
import time
import requests
from typing import Dict

from ..config import BRIA_API_TOKEN, BRIA_API_URL, OUTPUT_DIR


def image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def save_image_from_url(url: str, output_path: str) -> str:
    """Download image from URL and save locally."""
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def call_bria_api(payload: dict) -> dict:
    """Call Bria API for image generation (async V2 - polls for result)."""
    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }
    
    time.sleep(3)
    
    for attempt in range(3):
        try:
            response = requests.post(BRIA_API_URL, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            break
        except Exception as e:
            if attempt == 2:
                raise
            print(f"[call_bria_api] Request failed, retrying in 5s: {e}")
            time.sleep(5)
    
    data = response.json()
    
    if data.get("result", {}).get("url") or data.get("url"):
        return data
    
    status_url = data.get("status_url")
    if not status_url:
        raise ValueError(f"No status_url in response: {data}")
    
    print(f"[call_bria_api] Polling status: {status_url}")
    
    for i in range(18):
        time.sleep(7)
        
        try:
            status_response = requests.get(status_url, headers={"api_token": BRIA_API_TOKEN}, timeout=30)
            status_data = status_response.json()
        except Exception as e:
            print(f"[call_bria_api] Poll failed, retrying: {e}")
            time.sleep(5)
            continue
        
        status = status_data.get("status", "").lower()
        print(f"[call_bria_api] Status: {status}")
        
        if status in ("completed", "ready"):
            result = status_data.get("result", {})
            if isinstance(result, dict):
                image_url = result.get("url") or result.get("image_url")
            else:
                image_url = None
            
            if not image_url:
                image_url = (
                    status_data.get("url") or
                    status_data.get("result_url") or
                    status_data.get("image_url")
                )
            if image_url:
                return {"url": image_url}
            
            results = status_data.get("result", [])
            if isinstance(results, list) and results:
                return {"url": results[0].get("url")}
            raise ValueError(f"Completed but no URL: {status_data}")
        
        elif status in ("failed", "error"):
            raise ValueError(f"Image generation failed: {status_data}")
    
    raise TimeoutError("Image generation timed out after 90 seconds")


def generate_character_image(name: str, description: str, video_id: str) -> dict:
    """Generate a character reference image using Bria API."""
    print(f"[generate_character_image] Generating: {name}")
    
    safe_desc = description.replace("young", "").replace("girl", "person").replace("boy", "person")
    
    prompts = [
        f"Cartoon illustration of {name}, {safe_desc}, friendly expression, colorful, white background, digital art style",
        f"Animated character {name}, {safe_desc}, cartoon style, simple background",
        f"Friendly cartoon character, {safe_desc}, illustration style"
    ]
    
    output_path = str(OUTPUT_DIR / f"char_{name.lower().replace(' ', '_')}_{video_id}.png")
    
    for i, prompt in enumerate(prompts):
        try:
            print(f"[generate_character_image] Attempt {i+1}: {prompt[:50]}...")
            payload = {"prompt": prompt}
            data = call_bria_api(payload)
            image_url = data.get("url")
            
            if not image_url:
                raise ValueError(f"No image URL in response: {data}")
            
            save_image_from_url(image_url, output_path)
            print(f"[generate_character_image] Saved: {output_path}")
            return {"url": image_url, "local_path": output_path}
            
        except Exception as e:
            print(f"[generate_character_image] Attempt {i+1} failed: {e}")
            if i == len(prompts) - 1:
                raise
            time.sleep(4)
    
    raise ValueError("All prompt attempts failed")


def text_to_image(prompt: str, video_id: str, scene_index: int) -> str:
    """Generate scene image from text using Bria API."""
    print(f"[text_to_image] Generating scene {scene_index}")
    
    payload = {"prompt": prompt}
    
    try:
        data = call_bria_api(payload)
        image_url = data.get("url")
        
        if not image_url:
            raise ValueError(f"No image URL in response: {data}")
        
        output_path = str(OUTPUT_DIR / f"txt2img_{video_id}_{scene_index}.png")
        save_image_from_url(image_url, output_path)
        
        print(f"[text_to_image] Saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"[text_to_image] Error: {e}")
        raise


def image_to_image(prompt: str, character_urls: Dict[str, str], video_id: str, 
                   scene_index: int, gemini_session) -> str:
    """Generate scene image using character reference URLs via Bria API."""
    print(f"[image_to_image] Generating scene {scene_index} with characters: {list(character_urls.keys())}")
    
    char_list = list(character_urls.keys())
    
    try:
        selected_character = gemini_session.select_character_for_scene(prompt, char_list)
        print(f"[image_to_image] Selected character: {selected_character}")
    except:
        selected_character = char_list[0] if char_list else None
    
    if selected_character and selected_character in character_urls:
        reference_url = character_urls[selected_character]
        payload = {
            "prompt": f"{prompt}",
            "images": [reference_url]
        }
        print(f"[image_to_image] Using reference URL: {reference_url[:60]}...")
    else:
        payload = {"prompt": prompt}
    
    try:
        data = call_bria_api(payload)
        image_url = data.get("url")
        
        if not image_url:
            raise ValueError(f"No image URL in response: {data}")
        
        output_path = str(OUTPUT_DIR / f"scene_i2i_{video_id}_{scene_index}.png")
        save_image_from_url(image_url, output_path)
        
        print(f"[image_to_image] Saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"[image_to_image] Error: {e}, falling back to text_to_image")
        return text_to_image(prompt, video_id, scene_index)
