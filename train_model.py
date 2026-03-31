import numpy as np
import pickle
import csv

# 1. Load data
X_list = []
y_list = []

with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        # Expected format: [date, temp, humidity, pressure, wind]
        y_list.append(float(row[1])) 
        X_list.append([float(row[2]), float(row[3]), float(row[4])])

X = np.array(X_list)
y = np.array(y_list)
X = np.c_[np.ones(X.shape[0]), X] # Add Bias

# 2. Math (Normal Equation)
theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)

# 3. Save the weights
with open("model.pkl", "wb") as f:
    pickle.dump(theta, f)

print("SUCCESS: model.pkl has been created!")

