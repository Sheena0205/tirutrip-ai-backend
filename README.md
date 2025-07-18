# TiruTrip AI Planner - Backend 🕉️

This is the backend for the TiruTrip AI Planner. It is a Python API built with the FastAPI framework that receives user travel preferences and uses the Google Gemini API to generate a personalized itinerary.

## ✨ Key Features

- **FastAPI Server:** Provides a robust and fast API endpoint.
- **AI Integration:** Connects securely to the Google Gemini API.
- **Prompt Engineering:** Constructs detailed prompts to guide the AI into generating a structured JSON response.
- **Data-Driven:** Uses a local JSON file for a list of attractions to ensure accuracy.

## 🛠️ Technologies Used

- **Python**
- **FastAPI**
- **Google Gemini API**
- **python-dotenv**

## 🚀 How to Run Locally

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
py -m venv venv
.\venv\Scripts\activate

# Install required packages
pip install -r requirements.txt

# Create a .env file and add your GOOGLE_API_KEY
# GOOGLE_API_KEY="YOUR_API_KEY_HERE"

# Run the server
uvicorn main:app --reload
