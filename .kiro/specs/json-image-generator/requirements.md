# Requirements Document

## Introduction

This feature introduces an agentic AI-powered video generation system using Google ADK (Agent Development Kit). The current implementation generates isolated images for each scene, resulting in visually inconsistent videos that feel like slideshows. The new system uses a stateful AI agent that:
1. Receives a story prompt from the user
2. Generates character images first and stores them with names
3. Enhances and extends the story into scenes
4. For each scene: generates image (image-to-image with characters, or text-to-image if no characters), creates voiceover, multiplies image frames (24 × voice duration)
5. Merges all scene videos, merges all audio, combines video+audio
6. Delivers final video to user

Most code already exists - only the agentic AI orchestration and new image generation tools need implementation. Image generation functions will be left as stubs for manual implementation.

## Glossary

- **Video_Agent**: The ADK-based AI agent responsible for orchestrating the entire video generation pipeline
- **Session_Service**: The ADK component that manages conversation state and generated asset references
- **Runner**: The ADK runtime that executes the Video_Agent
- **LiveRequestQueue**: The ADK component for sending messages to the Video_Agent
- **Character_Reference**: A generated base image of a character stored with its name for reuse
- **Scene_Spec**: A JSON object containing visual properties for a scene's image generation
- **Image_To_Image_Tool**: Agent tool that generates images using character references as input
- **Text_To_Image_Tool**: Agent tool that generates images from text prompts (no character references)

## Requirements

### Requirement 1

**User Story:** As a video creator, I want an AI agent that orchestrates the entire video generation pipeline, so that I only need to provide a story prompt and receive a complete video.

#### Acceptance Criteria

1. WHEN a user provides a story prompt, THE Video_Agent SHALL initialize an ADK session and begin the video generation pipeline
2. WHEN the Video_Agent starts processing, THE Video_Agent SHALL store the video_id and all generated assets in the session state
3. WHEN any step completes, THE Video_Agent SHALL automatically proceed to the next step in the pipeline
4. WHEN the pipeline completes, THE Video_Agent SHALL deliver the final video path to the user

### Requirement 2

**User Story:** As a video creator, I want the agent to generate character images first, so that characters look consistent throughout the video.

#### Acceptance Criteria

1. WHEN a story prompt is received, THE Video_Agent SHALL analyze the story and identify all unique characters
2. WHEN characters are identified, THE Video_Agent SHALL generate a base Character_Reference image for each character
3. WHEN generating a Character_Reference, THE Video_Agent SHALL store the image path with the character name in session state
4. WHEN all characters are generated, THE Video_Agent SHALL proceed to story enhancement and scene generation

### Requirement 3

**User Story:** As a video creator, I want the agent to enhance and extend my story into detailed scenes, so that the video has rich narrative content.

#### Acceptance Criteria

1. WHEN character generation completes, THE Video_Agent SHALL enhance and extend the original story prompt
2. WHEN enhancing the story, THE Video_Agent SHALL break it into discrete scenes with clear visual descriptions
3. WHEN scenes are generated, THE Video_Agent SHALL create a Scene_Spec JSON for each scene containing visual properties
4. WHEN Scene_Specs are created, THE Video_Agent SHALL proceed to generate images for each scene

### Requirement 4

**User Story:** As a video creator, I want scene images generated using character references when characters are present, so that character appearance remains consistent.

#### Acceptance Criteria

1. WHEN a scene contains characters, THE Video_Agent SHALL use the Image_To_Image_Tool with stored Character_References as input
2. WHEN a scene contains no characters, THE Video_Agent SHALL use the Text_To_Image_Tool with the scene description
3. WHEN multiple characters appear in a scene, THE Video_Agent SHALL provide all relevant Character_References to the Image_To_Image_Tool
4. WHEN image generation completes, THE Video_Agent SHALL store the scene image path and proceed to voiceover generation

### Requirement 5

**User Story:** As a video creator, I want voiceover generated for each scene, so that the video has narration matching the visuals.

#### Acceptance Criteria

1. WHEN a scene image is generated, THE Video_Agent SHALL generate voiceover audio for that scene's narrative text
2. WHEN voiceover is generated, THE Video_Agent SHALL calculate the audio duration in seconds
3. WHEN audio duration is known, THE Video_Agent SHALL calculate frame count as 24 multiplied by duration
4. WHEN frame count is calculated, THE Video_Agent SHALL create scene video by repeating the image for that many frames

### Requirement 6

**User Story:** As a video creator, I want all scenes automatically assembled into a final video, so that I receive a complete video without manual editing.

#### Acceptance Criteria

1. WHEN all scene videos are generated, THE Video_Agent SHALL merge all scene videos into a single video file
2. WHEN all audio files are generated, THE Video_Agent SHALL merge all audio files into a single audio track
3. WHEN video and audio are merged separately, THE Video_Agent SHALL combine them into the final video
4. WHEN the final video is created, THE Video_Agent SHALL save it to the videos folder with the video_id as filename

### Requirement 7

**User Story:** As a video creator, I want to define visual properties in a structured JSON format, so that the agent has precise instructions for image generation.

#### Acceptance Criteria

1. WHEN the Video_Agent creates a Scene_Spec, THE Video_Agent SHALL include scene description, characters present, mood, and composition
2. WHEN a Scene_Spec is processed, THE Video_Agent SHALL validate required fields before passing to image generation tools
3. WHEN Scene_Spec contains invalid fields, THE Video_Agent SHALL use sensible defaults and log warnings
4. WHEN Scene_Spec is used, THE Video_Agent SHALL serialize it to JSON for debugging and logging

### Requirement 8

**User Story:** As a developer, I want the image generation tools to be implemented as stubs, so that I can manually implement the actual image generation logic.

#### Acceptance Criteria

1. WHEN the Image_To_Image_Tool is called, THE tool SHALL accept character reference paths and scene description as parameters
2. WHEN the Text_To_Image_Tool is called, THE tool SHALL accept scene description as parameter
3. WHEN either tool is called, THE tool SHALL return a placeholder image path for now
4. WHEN implementing tools, THE tool interface SHALL match the expected input/output format for future implementation

### Requirement 9

**User Story:** As a video creator, I want the system to maintain a character registry that maps character names to their reference images, so that the agent can automatically select the correct character images for each scene.

#### Acceptance Criteria

1. WHEN a character image is generated, THE Video_Agent SHALL call the store_character tool to save the character name, image path, and description to the Character_Registry
2. WHEN processing a scene, THE Video_Agent SHALL call the get_character_references tool with character names to retrieve matching character image paths
3. WHEN the Character_Registry contains a character matching a name in the scene, THE get_character_references tool SHALL return the stored image path for that character
4. WHEN no matching character is found in the Character_Registry, THE Video_Agent SHALL use Text_To_Image_Tool instead of Image_To_Image_Tool
