import numpy as np
import pickle
import csv

# Load CSV manually
X_list = []
y_list = []

with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        # row = [date, temp, humidity, pressure, wind]
        y_list.append(float(row[1]))
        X_list.append([float(row[2]), float(row[3]), float(row[4])])

X = np.array(X_list)
y = np.array(y_list)

# Add bias
X = np.c_[np.ones(X.shape[0]), X]

# Train using Normal Equation
theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

# Save model
pickle.dump(theta, open("model.pkl", "wb"))

print("Model trained")
