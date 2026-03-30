import numpy as np
import pickle

# load model
theta = pickle.load(open("model.pkl", "rb"))

# example input: humidity, pressure, wind
humidity = 60
pressure = 1010
wind = 5

X = np.array([1, humidity, pressure, wind])
prediction = X.dot(theta)

print("Predicted temperature:", prediction)
