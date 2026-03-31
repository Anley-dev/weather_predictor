from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np
import os
import datetime
import csv

app = Flask(__name__)
CORS(app)

# Load the weights (theta)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")

# Load model weights (the numpy array)
if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
else:
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({"status": "error", "message": "Model not found"})

        data = request.json
        h = float(data.get('humidity', 0))
        p = float(data.get('pressure', 0))
        w = float(data.get('wind', 0))

        # input_vector must match: [Bias, Humidity, Pressure, Wind]
        input_vector = np.array([1, h, p, w])

        # Manual math: Temp = Input_Vector DOT Theta
        prediction = np.dot(input_vector, model)
        rounded_pred = round(float(prediction), 2)

        # --- AUTO-LEARNING SECTION ---
        # Log this prediction back to data.csv for future training
        csv_path = os.path.join(BASE_DIR, "../data.csv")
        date_today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        try:
            with open(csv_path, "a", newline='') as f:
                writer = csv.writer(f)
                # Matches CSV format: Date, Temp, Hum, Pres, Wind
                writer.writerow([date_today, rounded_pred, h, p, w])
        except Exception as csv_err:
            print(f"Logging error: {csv_err}") 
        # -----------------------------

        return jsonify({
            "status": "success",
            "prediction": rounded_pred
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

