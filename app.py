from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def home():
    return "ML Weather API Running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    temp = data.get('temp', 0)

    # convert to correct format
    input_data = np.array([[temp]])

    prediction = model.predict(input_data)[0]

    return jsonify({
        "input": temp,
        "prediction": float(prediction)
    })

if __name__ == "__main__":
    app.run(debug=True)
