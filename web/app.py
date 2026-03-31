from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np
import os

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
            return jsonify({"status": "error", "message": "model.pkl not found!"}), 500
        
        data = request.json
        h = float(data.get('humidity', 0))
        p = float(data.get('pressure', 0))
        w = float(data.get('wind', 0))

        # input_vector must match: [Bias, Humidity, Pressure, Wind]
        input_vector = np.array([1, h, p, w])

        # Manual math: Temp = Input_Vector DOT Theta
        prediction = np.dot(input_vector, model)

        return jsonify({
            "status": "success",
            "prediction": round(float(prediction), 2)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)

