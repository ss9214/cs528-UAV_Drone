import os
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import time
import serial.tools.list_ports

features = []
labels = []
truncate = 275
#directions = ['left','right','up','down','forward','backward','turn_left','turn_right']
directions = ['up','down']



for k, direction in enumerate(directions):
    for i in range(1,81):
        df=pd.read_csv(f"./csv_data/{direction}_{i:02}.csv",usecols=['acce_x', 'acce_y', 'acce_z', 'gyro_x', 'gyro_y', 'gyro_z'])
        data = df[['acce_x', 'acce_y', 'acce_z', 'gyro_x', 'gyro_y', 'gyro_z']].values[:truncate]
        data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))

        # Populate lists with normalized data and labels
        features.append(data.flatten())
        labels.append(k)
X,y =  np.array(features), np.array(labels)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svm_classifier = SVC(kernel='rbf')

# Train the classifier
svm_classifier.fit(X_train, y_train)

# Perform prediction on the test set
y_pred = svm_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'SVM accuracy: {accuracy:.3%}')

# Plot the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, cmap="Blues")
plt.title('train')
plt.xlabel('pred')
plt.ylabel('actual')
plt.savefig('svm_confusion_matrix.png')
plt.close()


ser = serial.Serial('COM3', 115200)
while True:
    print("test1")
    start_time = time.time()
    input_data = []
    print("Collecting data...")
    # Collect data for 2 seconds
    while time.time() - start_time < 4:
        try:
            data = ser.readline().decode('utf-8').strip()
            data = data[30:-4].split(',')
            # Ensure we have exactly 6 values (acce_x, acce_y, acce_z, gyro_x, gyro_y, gyro_z)
            if len(data) == 6:
                try:
                    # Convert all values to float
                    data = [float(x) for x in data]
                    input_data.append(data)
                except ValueError:
                    continue
        except:
            continue
    if len(input_data) > 0:
        try:
            # Convert to numpy array and normalize like training data
            input_array = np.array(input_data)
            # Truncate or pad the input array to match min_length
            if len(input_array) > truncate:
                input_array = input_array[:truncate]
            elif len(input_array) < truncate:
                # Pad with zeros if the collected data is shorter
                padding = np.zeros((truncate - len(input_array), 6))
                input_array = np.vstack((input_array, padding))
            
            print(input_array)
            # Normalize the data
            if input_array.shape[1] == 6:  # Check if we have 6 features
                input_norm = (input_array - input_array.min(axis=0)) / (input_array.max(axis=0) - input_array.min(axis=0))
                
                # Make prediction
                prediction = svm_classifier.predict([input_norm.flatten()])
                
                # Convert numeric prediction back to direction
                #directions = ['left','right','up','down','forward','backward','turn_left','turn_right']
                directions = ['up','down']
                print(f"Predicted direction: {directions[prediction[0]]}")
            else:
                print("Invalid data shape")
        except Exception as e:
            print(f"Error processing data: {e}")
        
