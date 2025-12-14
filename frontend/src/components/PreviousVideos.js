import React, { useState } from 'react';
import { useVideo } from '../context/VideoContext';
import { Video, RefreshCw, X, Maximize2 } from 'lucide-react';

const getVideoUrl = (videoId) => {
  return `http://localhost:8000/public-video/${videoId}`;
};

const VideoModal = ({ video, onClose }) => {
  if (!video) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <div 
        className="relative w-full max-w-5xl mx-4 bg-dark-800 rounded-2xl overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          <h3 className="text-lg font-semibold text-white truncate pr-4">
            {video.message || 'Video'}
          </h3>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-white/70 hover:text-white" />
          </button>
        </div>
        <div className="p-4">
          <video
            src={getVideoUrl(video.video_id)}
            controls
            autoPlay
            className="w-full rounded-lg"
            style={{ maxHeight: '70vh' }}
          />
        </div>
        <div className="p-4 border-t border-white/10">
          <div className="flex items-center justify-between text-sm">
            <span className="text-white/60">
              Created: {new Date(video.created_at).toLocaleString()}
            </span>
            <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full">
              {video.status}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

const PreviousVideos = () => {
  const { videos, loading, fetchVideos } = useVideo();
  const [selectedVideo, setSelectedVideo] = useState(null);

  if (loading) {
    return (
      <div className="min-h-screen pt-20 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="w-8 h-8 border-2 border-primary-500/30 border-t-primary-500 rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-white/70">Loading videos...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen pt-20 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent mb-4">
            My Videos
          </h1>
          <p className="text-xl text-white/70 mb-4">
            All your generated videos
          </p>
          <button
            onClick={fetchVideos}
            disabled={loading}
            className="inline-flex items-center space-x-2 px-4 py-2 bg-primary-500/20 hover:bg-primary-500/30 text-primary-400 rounded-lg transition-all"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>

        {videos.length === 0 ? (
          <div className="card text-center py-16">
            <Video className="w-16 h-16 text-white/60 mx-auto mb-6" />
            <h3 className="text-xl font-semibold text-white mb-2">No Videos Yet</h3>
            <p className="text-white/60 mb-6">
              Create your first video
            </p>
            <a href="/" className="btn-primary">
              Create Video
            </a>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {videos.map((video) => (
              <div key={video.video_id} className="card group">
                <div className="relative bg-gradient-to-br from-primary-500/20 to-secondary-500/20 rounded-lg mb-4 flex items-center justify-center overflow-hidden">
                  {video.status === 'completed' && video.video_path ? (
                    <>
                      <video
                        src={getVideoUrl(video.video_id)}
                        className="w-full h-48 object-cover rounded-lg"
                        muted
                        onMouseEnter={(e) => e.target.play()}
                        onMouseLeave={(e) => { e.target.pause(); e.target.currentTime = 0; }}
                      />
                      <button
                        onClick={() => setSelectedVideo(video)}
                        className="absolute inset-0 flex items-center justify-center bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity"
                      >
                        <div className="p-3 bg-white/20 rounded-full backdrop-blur-sm">
                          <Maximize2 className="w-6 h-6 text-white" />
                        </div>
                      </button>
                    </>
                  ) : (
                    <div className="p-8 text-center h-48 flex flex-col items-center justify-center">
                      <Video className="w-12 h-12 text-white/40 mx-auto mb-2" />
                      <span className="text-white/60 text-sm capitalize">{video.status}</span>
                    </div>
                  )}
                </div>
                <h3 className="font-semibold text-white mb-2 truncate">
                  {video.message || 'Video'}
                </h3>
                <div className="flex items-center justify-between">
                  <span className="text-white/60 text-sm">
                    {new Date(video.created_at).toLocaleDateString()}
                  </span>
                  <span className={`text-xs px-2 py-1 rounded ${
                    video.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                    video.status === 'processing' ? 'bg-yellow-500/20 text-yellow-400' :
                    'bg-red-500/20 text-red-400'
                  }`}>
                    {video.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Video Modal */}
      <VideoModal video={selectedVideo} onClose={() => setSelectedVideo(null)} />
    </div>
  );
};

export default PreviousVideos;
