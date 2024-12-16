import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

def plot(filename, direction):
    metric = "accl"
    data = pd.read_csv(filename)

    N = len(data['accl_x'].values)

    yfx = fft(data[f'{metric}_x'].values)
    yfy = fft(data[f'{metric}_y'].values)
    yfz = fft(data[f'{metric}_z'].values)

    xf = fftfreq(N, d = 4/N)[:N//2]

    plt.figure().canvas.manager.set_window_title(f'FFT {filename[:-4]}')

    plt.plot(xf, 2.0/N * np.abs(yfx[0:N//2]), label = "X")
    plt.plot(xf, 2.0/N * np.abs(yfy[0:N//2]), label = "Y")
    plt.plot(xf, 2.0/N * np.abs(yfz[0:N//2]), label = "Z")

    plt.savefig(f'../graphs/2a/{metric}_fft_{direction}_{filename[-6:-4]}.png')

directions = ["up", "down", "left", "right"]

for direction in directions:
    plot(f"../{direction}/{direction}_01.csv", direction)
    plot(f"../{direction}/{direction}_06.csv", direction)