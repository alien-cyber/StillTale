"""Video generation routes."""

import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ..auth import get_current_user
from .. import database as db
from ..services.video_generator import generate_video_from_prompt

router = APIRouter(tags=["videos"])


class VideoRequest(BaseModel):
    prompt: str
    is_story: bool = False  # If True, use prompt as full story instead of generating one


class VideoResponse(BaseModel):
    video_id: str
    status: str
    message: str
    video_path: str | None = None
    created_at: str | None = None


def process_video_generation(video_id: str, prompt: str, is_story: bool = False):
    """Background task to generate video."""
    from ..services.video_generator import generate_video_from_prompt, generate_video_from_story
    try:
        if is_story:
            video_path = generate_video_from_story(prompt, video_id)
        else:
            video_path = generate_video_from_prompt(prompt, video_id)
        db.update_video_status(video_id, "completed", video_path)
    except Exception as e:
        print(f"[process_video_generation] Error: {e}")
        db.update_video_status(video_id, "failed")


@router.post("/generate-video", response_model=VideoResponse)
async def generate_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Start video generation (async)."""
    import uuid
    video_id = str(uuid.uuid4())[:8]
    
    db.create_video(video_id, current_user["id"], request.prompt)
    
    background_tasks.add_task(process_video_generation, video_id, request.prompt, request.is_story)
    
    return VideoResponse(
        video_id=video_id,
        status="processing",
        message=request.prompt[:100]
    )


@router.get("/my-videos", response_model=List[VideoResponse])
async def get_my_videos():
    """Get all videos (public - visible to all users)."""
    videos = db.get_all_videos()
    return [
        VideoResponse(
            video_id=v["video_id"],
            status=v["status"],
            message=v["message"],
            video_path=v["video_path"],
            created_at=str(v["created_at"])
        )
        for v in videos
    ]


@router.get("/video/{video_id}")
async def get_video(video_id: str, current_user: dict = Depends(get_current_user)):
    """Serve a video file (only to owner, requires auth header)."""
    video = db.get_video_by_id(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Check ownership
    if video["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if video["status"] != "completed" or not video["video_path"]:
        raise HTTPException(status_code=404, detail="Video not ready")
    
    if not os.path.exists(video["video_path"]):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        video["video_path"],
        media_type="video/mp4",
        filename=f"video_{video_id}.mp4"
    )


@router.get("/public-video/{video_id}")
async def get_video_with_token(video_id: str):
    """Serve a video file (public access)."""
    video = db.get_video_by_id(video_id)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    if video["status"] != "completed" or not video["video_path"]:
        raise HTTPException(status_code=404, detail="Video not ready")
    
    video_path = video["video_path"]
    print(f"[get_video] Serving video: {video_path}")
    
    if not os.path.exists(video_path):
        print(f"[get_video] File not found: {video_path}")
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        path=video_path,
        media_type="video/mp4",
        filename=f"video_{video_id}.mp4"
    )
