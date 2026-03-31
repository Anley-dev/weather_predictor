from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np
import os
import datetime
import csv

app = Flask(__name__)
CORS(app)

# 1. FIXED PATHING: Always look inside the current folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

# Initialize model as None
model = None

# Load the weights safely
if os.path.exists(model_path):
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
            print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading pickle: {e}")
else:
    print(f"CRITICAL: model.pkl not found at {model_path}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if model exists before doing math
        if model is None:
            return jsonify({"status": "error", "message": "Model not loaded on server"})

        data = request.json
        h = float(data.get('humidity', 0))
        p = float(data.get('pressure', 0))
        w = float(data.get('wind', 0))

        # Input vector: [Bias, Humidity, Pressure, Wind]
        input_vector = np.array([1, h, p, w])

        # MATH: Temp = Vector DOT Theta
        prediction = np.dot(input_vector, model)
        rounded_pred = round(float(prediction), 2)

        # --- AUTO-LEARNING (Safe for Cloud) ---
        # Look for CSV in the same folder to avoid "Permission Denied"
        csv_path = os.path.join(BASE_DIR, "data.csv") 
        date_today = datetime.datetime.now().strftime("%Y-%m-%d")

        try:
            with open(csv_path, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([date_today, rounded_pred, h, p, w])
        except Exception:
            # Silently fail CSV write on Vercel so the app doesn't crash
            pass 

        return jsonify({
            "status": "success",
            "prediction": rounded_pred
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Vercel needs this variable to be global
app = app

if __name__ == "__main__":
    app.run(debug=True, port=5000)

