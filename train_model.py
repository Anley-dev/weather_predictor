import numpy as np
import pickle
import csv
import os

X_list = []
y_list = []

# 1. Load and Clean Data
data_path = "data.csv"
if not os.path.exists(data_path):
    print("Error: data.csv not found!")
    exit()

with open(data_path, "r") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        # Skip empty rows or rows that don't have 5 columns (Date, Temp, Hum, Pres, Wind)
        if not row or len(row) < 5:
            continue
            
        try:
            # Skip the header row if it contains text like "date" or "temp"
            target_temp = float(row[1])
            features = [float(row[2]), float(row[3]), float(row[4])]
            
            y_list.append(target_temp)
            X_list.append(features)
        except ValueError:
            print(f"Skipping row {i} (Header or invalid data)")
            continue

# 2. Convert to Numpy
X = np.array(X_list)
y = np.array(y_list)

if len(X) < 2:
    print("Error: Need at least 2 rows of valid data to train!")
    exit()

# 3. Add Bias Column (The column of 1s)
X_b = np.c_[np.ones(X.shape[0]), X]

# 4. The Math: Normal Equation
# theta = (X^T * X)^-1 * X^T * y
try:
    theta = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)
    
    # 5. Save the new model
    with open("model.pkl", "wb") as f:
        pickle.dump(theta, f)
    
    print("--- SUCCESS ---")
    print(f"Model trained on {len(y_list)} rows.")
    print("Weights (Theta):", theta)
except np.linalg.LinAlgError:
    print("Math Error: Your data is too similar (Singular Matrix). Add more varied rows to data.csv!")

