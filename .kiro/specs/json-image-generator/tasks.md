# Implementation Plan

- [x] 1. Set up ADK dependencies and project structure





  - [x] 1.1 Add google-adk to requirements.txt


    - Add `google-adk` package dependency
    - _Requirements: 1.1_
  - [x] 1.2 Create agent module structure


    - Create `backend/services/agent/` directory
    - Create `__init__.py`, `agent.py`, `tools.py`, `models.py` files
    - _Requirements: 1.1_

- [x] 2. Implement data models and schemas







  - [x] 2.1 Create Scene_Spec and CharacterEntry models



    - Define Pydantic models for Scene_Spec, CharacterEntry, VideoGenerationState
    - Include validation for required fields
    - _Requirements: 7.1, 7.2_
  - [x]* 2.2 Write property test for Scene_Spec serialization round trip


    - **Property 4: Scene_Spec Serialization Round Trip**
    - **Validates: Requirements 7.4**
  - [x]* 2.3 Write property test for Scene_Spec required fields


    - **Property 5: Scene_Spec Required Fields**
    - **Validates: Requirements 7.1, 7.2**

- [x] 3. Implement Character Registry tools


  - [x] 3.1 Implement store_character tool


    - Create function that stores character name, image_path, description in session state
    - Use ToolContext to access session state
    - _Requirements: 2.3, 9.1_
  - [x] 3.2 Implement get_character_references tool

    - Create function that retrieves character image paths by names from session state
    - Return dict mapping character names to image paths
    - _Requirements: 9.2, 9.3_
  - [x]* 3.3 Write property test for Character Registry consistency

    - **Property 1: Character Registry Consistency**
    - **Validates: Requirements 2.3, 9.1, 9.2, 9.3**


- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement image generation tool stubs


  - [x] 5.1 Create generate_character_image stub

    - Define function signature accepting name, description, video_id
    - Return placeholder path string
    - Leave implementation empty for manual completion
    - _Requirements: 8.1, 8.3_
  - [x] 5.2 Create image_to_image_tool stub

    - Define function signature accepting scene_description, character_references dict, video_id, scene_index
    - Return placeholder path string
    - Leave implementation empty for manual completion
    - _Requirements: 8.1, 8.3_
  - [x] 5.3 Create text_to_image_tool stub

    - Define function signature accepting scene_description, video_id, scene_index
    - Return placeholder path string
    - Leave implementation empty for manual completion
    - _Requirements: 8.2, 8.3_


- [x] 6. Implement voiceover and video assembly tools
  - [x] 6.1 Implement generate_voiceover tool
    - Wrap existing text_to_audio function
    - Return tuple of (audio_path, duration)
    - _Requirements: 5.1, 5.2_
  - [x] 6.2 Implement assemble_scene_video tool
    - Calculate frame_count = round(24 * duration)
    - Create image list with repeated image path
    - Call existing images_to_video function
    - _Requirements: 5.3, 5.4_
  - [x]* 6.3 Write property test for frame count calculation
    - **Property 3: Frame Count Calculation**
    - **Validates: Requirements 5.3, 5.4**
  - [x] 6.4 Implement finalize_video tool
    - Call existing merge_audio_files function
    - Call existing merge_video_audio function
    - Save to videos/{video_id}.mp4
    - Call cleanup_files
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  - [x]* 6.5 Write property test for final video path format
    - **Property 7: Final Video Path Format**
    - **Validates: Requirements 6.4**

- [x] 7. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement Video_Agent
  - [x] 8.1 Create Video_Agent with ADK
    - Define Agent with name, model, tools list
    - Write comprehensive instruction for the pipeline
    - _Requirements: 1.1, 1.2, 1.3_
  - [x] 8.2 Implement agent initialization with session
    - Create SessionService (InMemorySessionService)
    - Create Runner with agent and session_service
    - Initialize session state with video_id and empty character_registry
    - _Requirements: 1.1, 1.2_
  - [x]* 8.3 Write property test for tool selection based on character presence
    - **Property 2: Tool Selection Based on Character Presence**
    - **Validates: Requirements 4.1, 4.2, 9.4**


- [x] 9. Integrate agent with existing API



  - [x] 9.1 Create agent runner endpoint


    - Add new endpoint or modify existing video generation endpoint
    - Initialize agent session and run pipeline
    - Return video_id and status
    - _Requirements: 1.4, 4.4_
  - [x] 9.2 Update video_generator.py to use agent

    - Replace current process_video with agent-based pipeline
    - Maintain backward compatibility with existing database updates
    - _Requirements: 1.3, 1.4_

- [x] 10. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
