import math
import numpy as np
from GraphPlot import plotHistogram

# add a window to the points
def addWindow(points):
    # use a window function on the data to make the data fit
    # TODO choose a better window function
    windowFunction = np.bartlett(len(points))
    for i, windowFactor in enumerate(windowFunction):
        points[i] = points[i] * windowFactor

    return points

# get the phi of the two points
def getPhi(adjacent, opposite):
    # Calculate the phi in degrees by doing: atan(o/a)
    # the absolute of o and a are needed to properly calculate the corner
    if(adjacent == 0):
        phi = 0
    else:    
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

    # plot the phis in a histogram
    #plotHistogram(phis, totalBins)

    rotatedY1 = []

    for i in range(0, len(yNS)):
        # the hypothenuse is the hyptohenuse of the North-South and East-West values
        hypotenuse = np.sqrt(np.square(yNS[i]) + np.square(yEW[i]))

        # get the corner in degrees of this point relative to the start
        # North-South is adjacent
        # East-West is opposite
        phi = getPhi(yNS[i], yEW[i])

        corner = maxPhi - phi
        length = np.sin(np.radians(corner)) * hypotenuse
        rotatedY1.append(length)

    rotatedY2 = []

    for i in range(0, len(yNS)):
        # the hypothenuse is the hyptohenuse of the North-South and East-West values
        hypotenuse = np.sqrt(np.square(yNS[i]) + np.square(yEW[i]))

        # get the corner in degrees of this point relative to the start
        # North-South is adjacent
        # East-West is opposite
        phi = getPhi(yNS[i], yEW[i])

        corner = maxPhi - phi
        length = np.cos(np.radians(corner)) * hypotenuse
        rotatedY2.append(length)

    return rotatedY1, rotatedY2