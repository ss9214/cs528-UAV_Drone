import numpy as np
import pandas as pd
from sklearn.svm import SVC
import serial
from time import sleep
from djitellopy import Tello
import keyboard
import time

# Function to load dataset
def load_data():

    directions = ["down","up","rightturn","leftturn","forward","backward","left","none"]
    features = []
    labels = []

    for k, direction in enumerate(directions):
        for i in range(1,81):
            df = pd.read_csv(f"../data/{direction}/{direction}_{i:02}.csv", usecols=['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z'])


            # Keep only accelerometer and gyroscope signals
            data = df[['accl_x', 'accl_y', 'accl_z', 'gyro_x', 'gyro_y', 'gyro_z']].iloc[:275].values.astype(np.float32)
            
            # Normalize data
            data = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
            
            # Populate lists with normalized data and labels
            features.append(data.flatten())
            labels.append(direction)

    return np.array(features), np.array(labels)

#SVC Training
print("Training ...")
X, Y = load_data()
clf = SVC(kernel='poly',C = 1, gamma=0.1, probability=True)
clf.fit(X, Y)
print("Training Complete...")


#Serial
port = "/dev/tty.usbserial-10" 
ser = serial.Serial(port, baudrate = 115200)
print("Recording ...")


#Drone Controls
def control_drone(direction):
    try:
        tello.connect()
        print("Drone connected.")
        print(f"Battery level: {tello.get_battery()}%")
        print("Press 't' to take off, 'l' to land, and 'q' to quit.")

        while True:

            print("Enter your move...")

            # Takeoff
            if keyboard.is_pressed('t'):
                try:
                    print("Taking off...")
                    tello.takeoff()
                except Exception as e:
                    print(f"Failed to take off: {e}")
            # Land
            elif keyboard.is_pressed('l'):
                try:
                    print("Landing...")
                    tello.land()
                except Exception as e:
                    print(f"Failed to land: {e}")
            # Move up
            elif direction == "up":
                try:
                    print("Moving up...")
                    tello.move_up(magnitude)
                except Exception as e:
                    print(f"Failed to move up: {e}")
            # Move down
            elif direction == "down":
                try:
                    print("Moving down...")
                    tello.move_down(magnitude)
                except Exception as e:
                    print(f"Failed to move down: {e}")
            # Move left
            elif direction == "leftturn": #actually left
                try:
                    print("Moving left...")
                    tello.move_left(magnitude)
                except Exception as e:
                    print(f"Failed to move left: {e}")
            # Move right
            elif direction == "rightturn": #actually right
                try:
                    print("Moving right...")
                    tello.move_right(magnitude)
                except Exception as e:
                    print(f"Failed to move right: {e}")
            # Move forward
            elif direction == "forward":
                try:
                    print("Moving forward...")
                    tello.move_forward(magnitude)
                except Exception as e:
                    print(f"Failed to move forward: {e}")
            # Move backward
            elif direction == "backward":
                try:
                    print("Moving backward...")
                    tello.move_back(magnitude)
                except Exception as e:
                    print(f"Failed to move backward: {e}")
            # Turn right
            elif direction == "right": #actually turnright
                try:
                    print("Rotating clockwise...")
                    tello.rotate_clockwise(90)
                except Exception as e:
                    print(f"Failed to rotate clockwise: {e}")
            # Turn left
            elif direction == "left": #actually turnleft
                try:
                    print("Rotating counter-clockwise...")
                    tello.rotate_counter_clockwise(90)
                except Exception as e:
                    print(f"Failed to rotate counter-clockwise: {e}")
            # Exit the loop
            elif keyboard.is_pressed('q'):
                try:
                    print("Exiting program...")
                    tello.land()
                    break
                except Exception as e:
                    print(f"Failed to quit: {e}")
            
    except Exception as e:
        print(f"an error occurred: {e}")
        tello.land()

    finally:
        # Ensure the drone lands safely before exiting
        print("Ensuring the drone is landed...")
        try:
            tello.land()
        except Exception as e:
            print(f"Error during landing: {e}")
        
        tello.end()



while True:
    try:
        input = []
        while len(input) < 275:
            data = ser.readline().decode('utf-8').strip()
            data = data[26:-4].split(',')
            if len(data) == 6:
                data = list(map(float, data))
                input.append(np.array(data))
        input = np.array(input)
        input = (input - input.min(axis=0)) / (input.max(axis=0) - input.min(axis=0))
        input = input.flatten()
        predict = clf.predict([input])[0]
        conf_score = clf.predict_proba([input])[0].max()
        if predict != "none" and conf_score > 0.7:
            control_drone(predict)
            sleep(1) #Buffer time to reset hand position
    except Exception as error:
        print(type(error).__name__)







