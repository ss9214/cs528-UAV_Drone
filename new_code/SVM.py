import os
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.decomposition import PCA
import time
import serial.tools.list_ports

features = []
labels = []
truncate = 275
directions = ['up','down','forward','backward']

# Data collection and preprocessing
for k, direction in enumerate(directions):
    for i in range(1,81):
        df=pd.read_csv(f"./csv_data/{direction}_{i:02}.csv",usecols=['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z'])
        data = df[['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z']].values[:truncate]
        
        # Store raw data for proper scaling
        features.append(data.flatten())
        labels.append(k)

X, y = np.array(features), np.array(labels)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 1. Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 2. Apply PCA
pca = PCA(n_components=0.95)  # Preserve 95% of variance
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# 3. Grid Search for best parameters
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.1, 0.01],
    'kernel': ['rbf', 'linear']
}

print("Starting Grid Search...")
grid_search = GridSearchCV(SVC(), param_grid, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(X_train_pca, y_train)

# Use best model
best_svm = grid_search.best_estimator_
y_pred = best_svm.predict(X_test_pca)

# Print results
print("\nBest parameters:", grid_search.best_params_)
print("Best cross-validation score:", grid_search.best_score_)
print("Test set accuracy:", accuracy_score(y_test, y_pred))

# Plot the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10,8))
sns.heatmap(conf_matrix, annot=True, cmap="Blues", 
            xticklabels=directions, 
            yticklabels=directions)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig('svm_confusion_matrix.png')
plt.close()

# Add this after your confusion matrix but before the real-time prediction code

# Calculate per-class metrics
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=directions))

# Calculate per-class accuracy
per_class_accuracy = conf_matrix.diagonal()/conf_matrix.sum(axis=1)
for direction, accuracy in zip(directions, per_class_accuracy):
    print(f"\n{direction} accuracy: {accuracy:.2%}")

# Find the most confused pairs
print("\nMost confused pairs:")
n_classes = len(directions)
confusion_pairs = []
for i in range(n_classes):
    for j in range(n_classes):
        if i != j:
            confusion_pairs.append((
                directions[i], 
                directions[j], 
                conf_matrix[i][j],
                f"{conf_matrix[i][j]/conf_matrix[i].sum():.2%}"
            ))

# Sort by number of confusions and print top 3
confusion_pairs.sort(key=lambda x: x[2], reverse=True)
print("\nTop 3 most confused pairs:")
for actual, predicted, count, percentage in confusion_pairs[:3]:
    print(f"Actual: {actual}, Predicted: {predicted}, Count: {count}, Percentage: {percentage}")
    
# Real-time prediction function
def preprocess_real_time_data(input_data, truncate):
    if len(input_data) > truncate:
        input_data = input_data[:truncate]
    elif len(input_data) < truncate:
        padding = np.zeros((truncate - len(input_data), 6))
        input_data = np.vstack((input_data, padding))
    
    # Flatten and scale using the same scaler
    input_flat = input_data.flatten().reshape(1, -1)
    input_scaled = scaler.transform(input_flat)
    
    # Apply PCA transformation
    input_pca = pca.transform(input_scaled)
    
    return input_pca

# Real-time prediction loop
ser = serial.Serial('COM3', 115200)
while True:
    print("test1")
    start_time = time.time()
    input_data = []
    print("Collecting data...")
    
    while time.time() - start_time < 4:
        try:
            data = ser.readline().decode('utf-8').strip()
            data = data[30:-4].split(',')
            if len(data) == 6:
                try:
                    data = [float(x) for x in data]
                    input_data.append(data)
                except ValueError:
                    continue
        except:
            continue
            
    if len(input_data) > 0:
        try:
            input_array = np.array(input_data)
            
            # Preprocess real-time data
            processed_input = preprocess_real_time_data(input_array, truncate)
            
            # Make prediction using best model
            prediction = best_svm.predict(processed_input)
            
            print(f"Predicted direction: {directions[prediction[0]]}")
        except Exception as e:
            print(f"Error processing data: {e}")