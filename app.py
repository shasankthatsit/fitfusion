
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from geopy.distance import geodesic
import random

app = Flask(__name__)
CORS(app)

# --- Constants ---
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Route: Analyze Symptoms ---
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    symptoms = data.get("symptoms", "")

    serious_keywords = [
        "chest pain", "shortness of breath", "bleeding", "severe", "fainting",
        "unconscious", "vomiting blood", "sudden vision loss", "paralysis", "seizure"
    ]
    is_serious = any(keyword in symptoms.lower() for keyword in serious_keywords)

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": f"Suggest advice and home remedies for: {symptoms}"}
            ]
        }
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        result = response.json()
        advice = result["choices"][0]["message"]["content"]
        return jsonify({"advice": advice, "is_serious": is_serious})
    except Exception as e:
        print("AI Error:", str(e))
        return jsonify({"advice": "Sorry, the AI could not generate a response.", "is_serious": is_serious})


# --- Route: Exercise Suggestion ---
@app.route('/exercise', methods=['POST'])
def get_exercise():
    data = request.json
    symptoms = data.get('symptoms', '').lower()

    if 'back pain' in symptoms:
        exercise = "Try gentle yoga stretches like Cat-Cow Pose and Child’s Pose."
    elif 'headache' in symptoms:
        exercise = "Practice breathing exercises like Anulom Vilom and Bhramari Pranayama."
    elif 'stress' in symptoms:
        exercise = "Try meditation, deep breathing, and Savasana pose."
    elif 'knee pain' in symptoms:
        exercise = "Do low-impact exercises like leg lifts and wall sits. Avoid squats."
    else:
        exercise = "Consult a physiotherapist or practice yoga like pranayama, surya namaskar based on your symptoms."

    return jsonify({"exercise": exercise})


# --- Route: Nearby Hospitals ---
@app.route('/hospitals', methods=['POST'])
def hospitals():
    data = request.json
    try:
        lat = float(data.get("latitude"))
        lon = float(data.get("longitude"))
    except:
        return jsonify({"hospitals": []})

    try:
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = f"""
        [out:json];
        (
          node["amenity"="hospital"](around:5000,{lat},{lon});
          way["amenity"="hospital"](around:5000,{lat},{lon});
          relation["amenity"="hospital"](around:5000,{lat},{lon});
        );
        out center;
        """

        headers = {
            "User-Agent": "FitFusionApp-Zaara/1.0 (zaara@example.com)"
        }

        res = requests.post(overpass_url, data=query, headers=headers)
        res.raise_for_status()
        data = res.json()

        hospitals = []
        for element in data["elements"]:
            name = element.get("tags", {}).get("name")
            if not name:
                continue

            if 'lat' in element and 'lon' in element:
                hlat, hlon = element['lat'], element['lon']
            else:
                hlat, hlon = element['center']['lat'], element['center']['lon']

            distance = geodesic((lat, lon), (hlat, hlon)).km
            rating = round(random.uniform(3.0, 5.0), 1)

            hospitals.append({
                "name": name,
                "lat": hlat,
                "lon": hlon,
                "distance": distance,
                "rating": rating
            })

        return jsonify({"hospitals": hospitals})

    except Exception as e:
        print("Hospital Fetch Error:", str(e))
        return jsonify({"hospitals": []})


# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
