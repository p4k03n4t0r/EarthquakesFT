import numpy as np
from scipy import signal

# normalize the provided y values by detrending and adding windowing
def normalize(y, totalPoints):
    # make sure the line stays around 0 (it is properly calibrated)
    y = signal.detrend(y)
    
    # use a window function on the data to make the data fit
    # TODO choose a better window function
    windowFunction = np.bartlett(totalPoints)
    for i, windowFactor in enumerate(windowFunction):
        y[i] = y[i] * windowFactor

    return y