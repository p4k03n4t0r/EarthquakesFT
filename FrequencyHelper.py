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
    # Calculate the phi in degrees by doing: atan(opposite/adjacent)
    # the absolute of o and a are needed to properly calculate the corner
    phi = np.degrees(np.arctan(abs(opposite)/abs(adjacent)))

    # decide the area where the point is located
    # area: North-East (+ 0 degrees)
    if(opposite >= 0 and adjacent >= 0):
        phi = 90 - phi
    # area: South-East (+ 90 degrees)
    if(opposite < 0 and adjacent >= 0):
        phi += 90
    # area: South-West (+ 180 degrees)
    if(opposite < 0 and adjacent < 0):
        phi = 270 - phi
    # area: North-West (+ 270 degrees)
    if(opposite >= 0 and adjacent < 0):
        phi += 270

    return phi

def rotate(yNS, yEW):   
    phis = []
    # find the largest values in the North-South and East-West displacements
    maxNS = abs(np.max(abs(yNS)))
    maxEW = abs(np.max(abs(yEW)))

    # calculate the Azimuth for each point
    for i in range(0, len(yNS)):
        # only take points which are 'peaks' by filtering out all corners of which the
        # amplitude is less than 50% of the max displacement of that axis
        if(abs(yNS[i]) > maxNS * 0.5 or abs(yEW[i]) > maxEW * 0.5):
            # get the corner in degrees of this point relative to the start
            # North-South is adjacent
            # East-West is opposite
            phi = getPhi(yNS[i], yEW[i])

            # add all valid phi's to the array
            if (not math.isnan(phi)):
                phis.append(phi)

    # divide the degrees in bins of 4 degrees wide 
    binDegrees = 10
    totalBins = int(360 / binDegrees)

    # calculate the histogram
    #TODO mod 180
    hist = np.histogram(phis, bins=totalBins)

    # find the index of the max value and map it back to degrees
    maxPhi = 360 - np.argmax(hist[0]) * binDegrees

    # plot the phis in a histogram
    #plotHistogram(phis, totalBins)

    rotatedX = []
    rotatedY = []
    
    for i in range(0, len(yNS)):
        # get the corner in degrees of this point relative to the start
        # North-South is adjacent
        # East-West is opposite
        phi = getPhi(yNS[i], yEW[i])

        # get the phi relative to the max phi
        phiDiff = phi - maxPhi

        # find the hypotenuse by calculating the pythagoram theorom of the distance
        # from the center (x=0, y=0) to the point
        hypotenuse = np.sqrt(np.square(yNS[i]) + np.square(yEW[i]))

        # calculate the distances from the point to the line to which the point must be rotated
        rotatedX.append(np.sin(np.radians(phiDiff)) * hypotenuse)
        rotatedY.append(np.cos(np.radians(phiDiff)) * hypotenuse)

    return rotatedX, rotatedY
