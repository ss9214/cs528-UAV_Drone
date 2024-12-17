import numpy as np
import pandas as pd
from sklearn.svm import SVC

# Function to load dataset
def load_data():

    directions = ["down","up","rightturn","leftturn","forward","backward","left", "right", "none"]
    features = []
    labels = []

    for k, direction in enumerate(directions):
        for i in range(1,81):
            df = pd.read_csv(f"data/{direction}/{direction}_{i:02}.csv", usecols=['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z'])


            # Keep only accelerometer and gyroscope signals
            data = df[['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z']].iloc[:275].values.astype(np.float32)
            
            # Normalize data
            data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
            
            # Populate lists with normalized data and labels
            features.append(data.flatten())
            labels.append(direction)

    return np.array(features), np.array(labels)

#SVC Training
#print("Training ...")
X, Y = load_data()
clf = SVC(kernel='poly',C = 1, gamma=0.1, probability=True)
clf.fit(X, Y)

