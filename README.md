# FitFusionApp Backend

FitFusionApp Backend is a Flask-based API that provides health-related services, including symptom analysis, exercise recommendations, and nearby hospital lookup. It integrates with an AI model via OpenRouter for symptom advice and uses Overpass API for hospital data.

## Features

- **Symptom Analysis**: Accepts user symptoms, checks for serious conditions, and provides AI-generated advice and home remedies using OpenRouter's API.
- **Exercise Suggestions**: Recommends exercises or yoga poses based on specific symptoms like back pain, headache, stress, or knee pain.
- **Nearby Hospitals**: Finds hospitals within a 5km radius of a given location using the Overpass API, including name, coordinates, distance, and a simulated rating.

## Tech Stack

- **Python 3.x**: Core programming language.
- **Flask**: Web framework for building the API.
- **Flask-CORS**: Handles Cross-Origin Resource Sharing.
- **Geopy**: Calculates distances between coordinates.
- **Requests**: Makes HTTP requests to external APIs.
- **OpenRouter API**: Provides AI-based symptom analysis.
- **Overpass API**: Fetches hospital location data.

## Prerequisites

- Python 3.6+
- Git
- A GitHub account (for cloning and contributing)
- An OpenRouter API key (sign up at [OpenRouter](https://openrouter.ai/))

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>

##Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

##Install Dependencies:
pip install flask flask-cors requests geopy

##Set Up Environment:
Replace the OPENROUTER_API_KEY in the code with your actual OpenRouter API key:
OPENROUTER_API_KEY = "your-api-key-here"

##Run the Application:
python app.py
The server will start at http://127.0.0.1:5000 in debug mode.
