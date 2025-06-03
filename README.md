# intellview
📌 IntelliView: AI-Powered Mock Interview Platform

**IntelliView** is an intelligent mock interview simulator designed to ease the stress of job interview preparation. It provides realistic, resume-aware, role-specific practice sessions using AI.


🚀 Overview

Job interviews can be overwhelming and lack effective, accessible practice tools. **IntelliView** bridges this gap with a smart, AI-powered mock interview system that simulates real interview conditions—leveraging Google Gemini API to dynamically generate personalized questions and evaluate candidate responses.


 🎯 Key Features

- 🎤 **AI-Generated Questions**: Tailored to the user's resume and selected job role
- ⏱ **Time-Bound Interactions**: Simulate real interview pressure with timed sessions
- 📋 **Resume Upload Support**: Accepts user resume for generating contextual questions
- 🧠 **Feedback System**: Automated scoring, feedback, suggestions, and sample answers
- 🌐 **Browser-Based**: Fully responsive front-end with no installation required
- 🎥 **Webcam + Mic Input**: Capture real-time responses for authenticity



🧰 Tech Stack

| Layer        | Technology                 |
|--------------|-----------------------------|
| Frontend     | HTML, CSS, JavaScript       |
| Backend      | Python (Flask)              |
| AI Engine    | Gemini API (Google LLM)     |
| Media Input  | JavaScript Web APIs (Webcam, Mic) |
| Deployment   | Browser-based (local or server-hosted) |


⚙️ Setup Instructions


1. Clone the Repository

    git clone https://github.com/your-username/intelliview.git
    cd intelliview

2. Install Python Dependencies

Make sure Python 3.7+ is installed.

    pip install -r requirements.txt


3. Install & Run MongoDB

  1. Download from https://www.mongodb.com/try/download/community
   
  2. Install and start the MongoDB server: by running mongosh on MongoDB shell

4. Run the Application

    python app.py

Then open your browser and navigate to:

    http://localhost:5000