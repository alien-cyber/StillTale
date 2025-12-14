# VideoGen AI Frontend

A beautiful React frontend for AI-powered video generation with Tailwind CSS.

## Features

- 🎨 **Modern Design** - Beautiful glass morphism UI with gradient effects
- 🔐 **Authentication** - Login and registration system
- 🎬 **Video Creation** - Simple prompt-based video generation
- 📹 **Video Library** - View and manage your generated videos
- 📱 **Responsive** - Works perfectly on all devices
- ⚡ **Fast** - Optimized with React 18 and modern tooling

## Tech Stack

- React 18
- React Router DOM
- Tailwind CSS
- Axios
- Lucide React Icons

## Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## Backend Integration

The frontend expects a backend running on `http://localhost:8000` with the following endpoints:

- `POST /login` - User authentication
- `POST /register` - User registration
- `POST /generate-video` - Create new video
- `GET /videos` - Get user's videos
- `DELETE /videos/{id}` - Delete a video

## Project Structure

```
src/
├── components/
│   ├── Dashboard.js      # Main video creation page
│   ├── Login.js          # Authentication page
│   ├── Navbar.js         # Navigation component
│   └── PreviousVideos.js # Video library page
├── context/
│   ├── AuthContext.js    # Authentication state management
│   └── VideoContext.js   # Video state management
├── App.js                # Main app component
└── index.js              # Entry point
```

## Design Features

- **Glass Morphism** - Translucent cards with backdrop blur
- **Gradient Backgrounds** - Beautiful color transitions
- **Smooth Animations** - Hover effects and transitions
- **Modern Icons** - Lucide React icon set
- **Responsive Grid** - Adaptive layouts for all screen sizes

## Customization

The app uses a custom Tailwind configuration with:
- Custom color palette (primary, secondary, dark)
- Custom animations and keyframes
- Glass effect utilities
- Custom button and input styles

Enjoy creating amazing videos! 🎬✨ 