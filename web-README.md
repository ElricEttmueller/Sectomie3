# Sectomie Web Interface

A simple web interface for the Sectomie Cultivation Sect Management System.

## Project Structure

The web interface consists of:

- **Backend**: Flask API that exposes the core Python functionality
- **Frontend**: Vue.js application with a cultivation-themed UI

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```
   python app.py
   ```
   The API will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm run serve
   ```
   The web interface will be available at http://localhost:8080

## Features

- View all cultivation sects and their details
- View all disciples and their cultivation progress
- Perform cultivation actions (cultivate, breakthrough)
- Manage sect resources
- Track cultivation progress

## Background Images

For the best visual experience, add your own cultivation-themed background images to:
```
frontend/public/assets/backgrounds/
```

Recommended image names:
- mountain.jpg
- temple.jpg
- cloud.jpg

## Next Steps

This is a simple implementation that can be extended with:

1. More detailed cultivation mechanics
2. Sect wars and tournaments
3. Disciple recruitment system
4. More advanced resource management
5. Animation effects for cultivation actions
