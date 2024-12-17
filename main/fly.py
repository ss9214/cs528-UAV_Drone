from train import clf
from djitellopy import Tello
import time
from time import sleep
import serial
import numpy as np
import keyboard

#Connect to Drone
try:
    tello = Tello()
    tello.connect()
    print("Drone connected.")
    print(f"Battery level: {tello.get_battery()}%")
except Exception as e:
    print(f"Failed to connect Tello: {e}")

#Take Off
try:
    tello.takeoff()
except Exception as e:
    print(f"Failed to take off: {e}")

#Quit
if keyboard.is_pressed('q'):
        print("Ensuring the drone is landed...")
        try:
            Tello.land()
        except Exception as e:
            print(f"Error during landing: {e}")

        print("Closing connection to the drone...")
        tello.end()

#Drone Controls function
def control_drone(direction, magnitude=30): 
    
    #else-if statements for directions:
    # Takeoff
    if direction == "up":
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
    #end of else-if statements
    
    # Quit
    if keyboard.is_pressed('q'):
        print("Ensuring the drone is landed...")
        try:
            Tello.land()
        except Exception as e:
            print(f"Error during landing: {e}")

        print("Closing connection to the drone...")
        tello.end()


#Data Collection:

#Serial
port = "/dev/tty.usbserial-10" 
ser = serial.Serial('COM3', baudrate = 115200)
print("Recording ...")

start_time = time.time()

while True:
    try:
        input = []
        #print("Recording...")
        while len(input) < 275:
            data = ser.readline().decode('utf-8').strip()
            data = data[26:-4].split(',')
            if len(data) == 6:
                data = list(map(float, data))
                input.append(np.array(data))
        input = np.array(input)
        #print(input)
        input = (input - input.min(axis=0)) / (input.max(axis=0) - input.min(axis=0))
        input = input.flatten()
        predict = clf.predict([input])[0]
        conf_score = clf.predict_proba([input])[0].max()
        if predict != "none" and conf_score > 0.7:
            control_drone(predict)
            print(predict)
            print("Wait...")
            sleep(1) #Buffer time to reset hand position
    except Exception as error:
        print(type(error).__name__)





