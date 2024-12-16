import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Extract CSV values

def plot(filename, direction):
    metric = "gyro"
    data = pd.read_csv(filename)
    interval = 4/len(data[f'{metric}_x'].values) #seconds

    time = np.arange(0, (len(data[f'{metric}_x'].values)) * interval, interval)

    plt.figure().canvas.manager.set_window_title(f'Acceleration-Time Domain {filename[:-4]}')

    plt.plot(time, data[f'{metric}_x'].values, label = "X")
    plt.plot(time, data[f'{metric}_y'].values, label = "Y")
    plt.plot(time, data[f'{metric}_z'].values, label = "Z")

    plt.savefig(f'../graphs/2b/{metric}_time_{direction}_{filename[-6:-4]}.png')

direction = "down"
plot(f"../{direction}/{direction}_01.csv", direction)
plot(f"../{direction}/{direction}_06.csv", direction)