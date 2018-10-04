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
#plot(ySW, yNS)

phis = []

# calculate the Azimuth for each point
for i in range(0, len(x)):
    # North-South is aanliggende
    aanliggende = yNS[i]
    # East-West is overstaande
    overstaande = yEW[i]

    # Calculate the phi in degrees by doing: atan(o/a)
    # the absolute of o and a are needed to properly calculate the corner
    phi = np.degrees(np.arctan(abs(overstaande)/abs(aanliggende)))

    # decide the area where the point is located
    # area: North-East (+ 0 degrees)
    if(overstaande >= 0 and aanliggende >= 0):
        phi += 0
    #area: South-East (+ 90 degrees)
    if(overstaande >= 0 and aanliggende < 0):
        phi += 90
    # area: South-West (+ 180 degrees)
    if(overstaande < 0 and aanliggende < 0):
        phi += 180
    # area: North-West (+ 270 degrees)
    if(overstaande < 0 and aanliggende >= 0):
        phi += 270

    if (not math.isnan(phi)):
        phis.append(phi)

# divide the degrees in bins of 4 degrees wide 
binDegrees = 4
totalBins = int(360 / binDegrees)

# calculate the histogram
hist = np.histogram(phis, bins=totalBins)

# find the index of the max value and map it back to degrees
maxPhi = np.argmax(hist[0]) * binDegrees
print(maxPhi)

# plot the phis in a histogram
plt.hist(phis, bins=totalBins)
plt.show()