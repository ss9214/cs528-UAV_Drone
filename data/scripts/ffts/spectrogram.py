import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import spectrogram

import math

def plot(filename, direction, metric):
    data = pd.read_csv(filename)

    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    fig.suptitle(f'Spectrogram of {"Acceleration" if metric == "accl" else "Gyroscope"} Data from {filename}', fontsize=16)
    nperseg = 256
    dt = 4/len(data['accl_x'].values)
    for i, axis in enumerate(['accl_x', 'accl_y', 'accl_z']):
        f, t, Sxx = spectrogram(data[axis], fs=1/dt, nperseg=nperseg, noverlap=nperseg//2)
        im = axs[i].pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud', cmap='viridis')
        axs[i].set_xlabel('Time (s)')
        axs[i].set_ylabel('Frequency (Hz)')
        axs[i].set_title(f'{axis} Spectrogram')
        fig.colorbar(im, ax=axs[i], label='Intensity (dB)')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'../graphs/{"2c" if metric == "accl" else "2d"}/{metric}_spectrogram_{direction}_{filename[-6:-4]}.png')

for metric in ["accl", "gyro"]:
    for direction in ["up", "down", "left", "right"]:
        plot(f"../{direction}/{direction}_01.csv", direction, metric)
        plot(f"../{direction}/{direction}_06.csv", direction, metric)