import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Initializations ---
app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class ItineraryRequest(BaseModel):
    days: str
    interests: list[str]
    startDate: str

# --- Helper Functions ---
# Note: If you decided not to use the places.json file, you can delete this function
# and follow the "hardcoding" instructions from before.
def get_places_data():
    with open("places.json", "r") as f:
        return json.load(f)

def create_prompt(request: ItineraryRequest, places: list):
    prompt = f"""
    You are an expert Tirupati travel planner. Your task is to create a personalized itinerary based on the user's preferences.

    User Preferences:
    - Number of Days: {request.days}
    - Interests: {', '.join(request.interests)}
    - Travel Start Date: {request.startDate}

    Available Places in and around Tirupati (JSON format):
    {json.dumps(places, indent=2)}

    Instructions:
    1. Create a logical, day-by-day itinerary.
    2. Prioritize the main Tirumala Temple darshan.
    3. Group places that are geographically close.
    4. Suggest timings and include buffer time for travel and meals.
    5. Recommend one authentic local restaurant for lunch or dinner each day.
    6. The final output must be only a valid JSON object, with no extra text or markdown like ```json.

    Required JSON Output Structure:
    {{
      "itinerary": [
        {{
          "day": 1,
          "theme": "A brief theme for the day",
          "schedule": [
            {{"time": "08:00 - 09:00", "activity": "Breakfast and start journey"}},
            {{"time": "09:00 - 14:00", "activity": "Activity Name", "details": "A brief detail about the place."}}
          ]
        }}
      ]
    }}
    """
    return prompt

# --- API Endpoints ---
@app.post("/api/generate-itinerary")
async def generate_itinerary(request: ItineraryRequest):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Note: If you are not using places.json, make sure you modified this part
        # according to the previous instructions.
        places = get_places_data()
        prompt = create_prompt(request, places)
        response = model.generate_content(prompt)
        
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "")
        itinerary_json = json.loads(cleaned_response_text)
        
        return itinerary_json

    except Exception as e:
        print(f"An error occurred: {e}")
        return {{"error": "Failed to generate itinerary. Please check the backend server logs."}}