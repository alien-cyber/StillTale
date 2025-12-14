import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const VideoContext = createContext();

export const useVideo = () => {
  const context = useContext(VideoContext);
  if (!context) {
    throw new Error('useVideo must be used within a VideoProvider');
  }
  return context;
};

export const VideoProvider = ({ children }) => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  const generateVideo = async (prompt, isStory = false) => {
    setGenerating(true);
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8000/generate-video', {
        prompt,
        is_story: isStory
      }, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      const newVideo = response.data;
      setVideos(prev => [newVideo, ...prev]);
      return { success: true, video: newVideo };
    } catch (error) {
      console.error('Video generation error:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Video generation failed' 
      };
    } finally {
      setGenerating(false);
    }
  };

  const fetchVideos = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:8000/my-videos');
      setVideos(response.data);
    } catch (error) {
      console.error('Fetch videos error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch videos when component mounts (public - no auth needed)
    fetchVideos();
  }, []);

  const value = {
    videos,
    loading,
    generating,
    generateVideo,
    fetchVideos
  };

  return (
    <VideoContext.Provider value={value}>
      {children}
    </VideoContext.Provider>
  );
}; 