import React, { useState } from 'react';
import { useVideo } from '../context/VideoContext';
import { Sparkles, Video, Wand2, Clock, CheckCircle, BookOpen } from 'lucide-react';

const Dashboard = () => {
  const [prompt, setPrompt] = useState('');
  const [isStoryMode, setIsStoryMode] = useState(false);
  const { generateVideo, generating } = useVideo();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    const result = await generateVideo(prompt, isStoryMode);
    if (result.success) {
      setPrompt('');
    }
  };

  const examplePrompts = [
    "A majestic dragon flying over a medieval castle at sunset",
    "A futuristic city with flying cars and neon lights",
    "A peaceful forest with butterflies and flowers",
    "An underwater scene with colorful fish and coral reefs",
    "A space station orbiting Earth with stars in the background"
  ];

  const exampleStory = `Luna, a young girl with silver hair, walked through the enchanted forest. She discovered a friendly dragon named Ember with shimmering red scales resting by a crystal lake. Together they embarked on an adventure to find the lost star that fell from the sky.`;

  return (
    <div className="min-h-screen pt-20 pb-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl mb-6 shadow-2xl">
            <Wand2 className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-400 to-secondary-400 bg-clip-text text-transparent mb-4">
            Create Your Video
          </h1>
          <p className="text-xl text-white/70 max-w-2xl mx-auto">
            Transform your imagination into stunning videos with AI
          </p>
        </div>

        {/* Mode Toggle */}
        <div className="flex justify-center mb-8">
          <div className="flex bg-dark-700 rounded-lg p-1">
            <button
              onClick={() => setIsStoryMode(false)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-300 ${
                !isStoryMode 
                  ? 'bg-primary-500 text-white shadow-lg' 
                  : 'text-white/60 hover:text-white'
              }`}
            >
              <Sparkles size={16} />
              <span>From Prompt</span>
            </button>
            <button
              onClick={() => setIsStoryMode(true)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-300 ${
                isStoryMode 
                  ? 'bg-primary-500 text-white shadow-lg' 
                  : 'text-white/60 hover:text-white'
              }`}
            >
              <BookOpen size={16} />
              <span>From Story</span>
            </button>
          </div>
        </div>

        {/* Video Creation Form */}
        <div className="card mb-12">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-lg font-semibold text-white mb-3">
                {isStoryMode ? 'Write Your Story' : 'Describe Your Video'}
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className={`input-field resize-none ${isStoryMode ? 'min-h-[200px]' : 'min-h-[120px]'}`}
                placeholder={isStoryMode 
                  ? "Write your full story here. Include character names and descriptions for best results..."
                  : "Describe the video you want to create..."
                }
                required
              />
              {isStoryMode && (
                <p className="text-white/50 text-sm mt-2">
                  Tip: Include character names with brief descriptions for consistent visuals across scenes.
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={generating || !prompt.trim()}
              className="btn-primary w-full flex items-center justify-center space-x-3 text-lg py-4"
            >
              {generating ? (
                <>
                  <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-6 h-6" />
                  <span>Generate Video</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Examples */}
        <div className="card">
          <h3 className="text-xl font-semibold text-white mb-4 flex items-center space-x-2">
            <Video className="w-5 h-5 text-primary-400" />
            <span>{isStoryMode ? 'Example Story' : 'Example Prompts'}</span>
          </h3>
          
          {isStoryMode ? (
            <button
              onClick={() => setPrompt(exampleStory)}
              className="w-full text-left p-4 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 hover:border-primary-500/30 transition-all duration-300"
            >
              <p className="text-white/80 text-sm leading-relaxed">
                {exampleStory}
              </p>
            </button>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {examplePrompts.map((example, index) => (
                <button
                  key={index}
                  onClick={() => setPrompt(example)}
                  className="text-left p-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 hover:border-primary-500/30 transition-all duration-300 group"
                >
                  <p className="text-white/80 group-hover:text-white text-sm">
                    {example}
                  </p>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-500/20 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Sparkles className="w-6 h-6 text-primary-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">AI Powered</h3>
            <p className="text-white/60 text-sm">
              Advanced AI technology creates stunning videos from your descriptions
            </p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-secondary-500/20 rounded-xl flex items-center justify-center mx-auto mb-4">
              <Clock className="w-6 h-6 text-secondary-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">Fast Generation</h3>
            <p className="text-white/60 text-sm">
              Get your videos in minutes, not hours
            </p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-500/20 rounded-xl flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-6 h-6 text-primary-400" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">High Quality</h3>
            <p className="text-white/60 text-sm">
              Professional-grade videos with stunning visuals
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
