import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import copy
import math
from scipy import signal

# read a file in the format received from Wilber3: http://ds.iris.edu/wilber3
def getWilberData(fileName):
    f = open(fileName, "r") 
    y = []
    # skip some meta data lines
    skipTillLine = 8
    for i, line in enumerate(f):
        if(i <= skipTillLine):
            continue
        # remove line breaks and parse to a number
        y.append(float(line.replace("\n","")))
    
    return y

def getWilberTotalPoints(fileName):
    f = open(fileName, "r") 
    for i, line in enumerate(f):
        if(i == 3):
            return float(line.replace("# sample_count: ","").replace("\n",""))

def getWilberFrequency(fileName):
    f = open(fileName, "r") 
    for i, line in enumerate(f):
        if(i == 4):
            return 1/float(line.replace("# sample_rate_hz: ","").replace("\n",""))

# get the phi of the two points
def getPhi(adjacent, opposite):
    # Calculate the phi in degrees by doing: atan(o/a)
    # the absolute of o and a are needed to properly calculate the corner
    phi = np.degrees(np.arctan(abs(opposite)/abs(adjacent)))

    # decide the area where the point is located
    # area: North-East (+ 0 degrees)
    if(opposite >= 0 and adjacent >= 0):
        phi += 0
    #area: South-East (+ 90 degrees)
    if(opposite >= 0 and adjacent < 0):
        phi += 90
    # area: South-West (+ 180 degrees)
    if(opposite < 0 and adjacent < 0):
        phi += 180
    # area: North-West (+ 270 degrees)
    if(opposite < 0 and adjacent >= 0):
        phi += 270

    return phi

# plot the provided x and y in a graph and show it
def plot(x, y):
    plt.plot(x, y)
    plt.grid()
    plt.show()

file1 = "Data/IC.HIA..BHE.M.1995-10-09T154841.003000.csv"
file2 = "Data/IC.HIA..BHN.M.1995-10-09T154841.003000.csv"

# simulate an amount of points
totalPoints = getWilberTotalPoints(file1)
frequency = getWilberFrequency(file1)
x = np.linspace(0, frequency * totalPoints, totalPoints)
yNS = getWilberData(file1)
yEW = getWilberData(file2)

# make sure the signal is properly calibrated (stays around 0)
yNS = signal.detrend(yNS)
yEW = signal.detrend(yEW)

# use a window function on the data to make the data fit
windowFunction = np.bartlett(totalPoints)
for i, windowFactor in enumerate(windowFunction):
    yNS[i] = yNS[i] * windowFactor

for i, windowFactor in enumerate(windowFunction):
    yEW[i] = yEW[i] * windowFactor

# plot of the earthquake Where the Y-axis is the North-South displacement
# and the X-asix the East-West displacement
plot(yEW, yNS)

phis = []

# calculate the Azimuth for each point
for i in range(0, len(x)):
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
plt.hist(phis, bins=totalBins)
plt.show()

rotatedY1 = []

for i in range(0, len(x)):
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

for i in range(0, len(x)):
    # the hypothenuse is the hyptohenuse of the North-South and East-West values
    hypotenuse = np.sqrt(np.square(yNS[i]) + np.square(yEW[i]))

    # get the corner in degrees of this point relative to the start
    # North-South is adjacent
    # East-West is opposite
    phi = getPhi(yNS[i], yEW[i])

    corner = phiLine - phi
    length = np.sin(np.radians(corner)) * hypotenuse
    rotatedY2.append(length)

plot(rotatedY1, rotatedY2)

#plt.plot(range(0, len(yNS)), yNS)
#plt.plot(range(0, len(yEW)), yEW)
#plt.grid()
#plt.show()
#plt.plot(range(0, len(rotatedY1)), rotatedY1)
#plot(range(0, len(rotatedY2)), rotatedY2)