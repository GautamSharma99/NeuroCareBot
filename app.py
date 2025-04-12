# app.py
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Replace with your actual API key
API_KEY = "AIzaSyBnbRuvRY_4LxRSJt4wePIjcnz9AK7Eydo"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Sample patient data
patient_profile = {
    "age": 45,
    "gender": "Male",
    "weight": "82kg",
    "known_conditions": ["Type 2 Diabetes", "Hypertension"],
    "recent_vitals": {
        "blood_pressure": "145/90",
        "glucose_level": "160 mg/dL",
        "heart_rate": "88 bpm"
    }
}

def format_patient_data(profile):
    vitals = profile["recent_vitals"]
    return f"""
Age: {profile['age']}
Gender: {profile['gender']}
Weight: {profile['weight']}
Known Conditions: {", ".join(profile['known_conditions'])}
Recent Vitals:
  - Blood Pressure: {vitals['blood_pressure']}
  - Glucose Level: {vitals['glucose_level']}
  - Heart Rate: {vitals['heart_rate']}
"""

def generate_health_response(query):
    prompt = f"""
    Interact with the patient as a human for non-medical questions.
    Answer the following health-related question based on the patient's profile and health data, if asked:
    Question: {query}
    Patient Profile:
    {format_patient_data(patient_profile)}
    Provide a concise answer focusing on:
    1. Direct response to the question
    2. Relevant health insights from the data
    3. Personalized recommendations if applicable
    4. Any necessary precautions or warnings
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error occurred: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('message', '')
    response = generate_health_response(query)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)