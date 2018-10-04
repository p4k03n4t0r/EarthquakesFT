import math
import numpy as np
from GraphPlot import plotHistogram
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

# get the phi of the two points
def getPhi(adjacent, opposite):
    # Calculate the phi in degrees by doing: atan(o/a)
    # the absolute of o and a are needed to properly calculate the corner
    phi = np.degrees(np.arctan(abs(opposite)/abs(adjacent)))

    # decide the area where the point is located
    # area: North-East (+ 0 degrees)
    if(opposite >= 0 and adjacent >= 0):
        phi += 0
    # area: South-East (+ 90 degrees)
    if(opposite >= 0 and adjacent < 0):
        phi += 90
    # area: South-West (+ 180 degrees)
    if(opposite < 0 and adjacent < 0):
        phi += 180
    # area: North-West (+ 270 degrees)
    if(opposite < 0 and adjacent >= 0):
        phi += 270

    return phi

def rotate(yNS, yEW):   
    phis = []

    # calculate the Azimuth for each point
    for i in range(0, len(yNS)):
        # get the corner in degrees of this point relative to the start
        # North-South is adjacent
        # East-West is opposite
        phi = getPhi(yNS[i], yEW[i])

        # add all valid phi's to the array
        if (not math.isnan(phi)):
            phis.append(phi)

    # divide the degrees in bins of 4 degrees wide 
    binDegrees = 4
    totalBins = int(360 / binDegrees)

    # calculate the histogram
    hist = np.histogram(phis, bins=totalBins)

    # find the index of the max value and map it back to degrees
    maxPhi = np.argmax(hist[0]) * binDegrees
    phiLine = maxPhi + 90

    # plot the phis in a histogram
    plotHistogram(phis, totalBins)