import numpy as np
from FileReader import getFilesPerStation, getData, getTotalPoints, getPointsPerSecond
from FrequencyHelper import normalize, rotate
from GraphPlot import plot, plotDisplacement
from FileRetriever import retrieveWilberData

# he folder in which the earthquake data can be found
folder = "Data"
#retrieveWilberData("paul/2018-09-15-mb42-adriatic-sea-2/timeseries_data/", folder)

# lists for the magnitudes and frequencies, which can be used to plot the graph
magnitudes = []
frequencies = []
highestFrequencies = []

filesPerStation = getFilesPerStation(folder)
# the North-South and East-West files of a station 
for fileNS, fileEW in filesPerStation:
    # simulate an amount of points based on the files parameters
    # if the total amount of points are not equal, ignore these measurements
    if(getTotalPoints(fileNS) != getTotalPoints(fileEW)):
        print("Different amount of points for files: " + fileNS + " and " + fileEW 
            + " (these will be ignored)")
        continue
    totalPoints = getTotalPoints(fileNS)

    pointsPerSecond = getPointsPerSecond(fileNS)

    # get the magnitude from the file
    x = np.linspace(0, pointsPerSecond * totalPoints, totalPoints)
    # normalize the data by detrending and windowing
    yNS = normalize(getData(fileNS), totalPoints)
    yEW = normalize(getData(fileEW), totalPoints)

    # plot the displacement, North-Sound on the y-axis and East-West on the x-axis
    #plotDisplacement(yNS, yEW)
    y1, y2 = rotate(yNS, yEW)
    continue
    y = yNS

    magnitudes.append([x, y])

    # calculate the Fourier Transforms of the sinus function
    # which will result in a list of points for each frequency, where
    # the x-axis represents real numbers and the y-axis imaginary numbers
    # only calculate real numbers, thus use the rfft instead of fft
    f = np.fft.rfft(y)

    # calculate the coördinates for each point
    # since the real fourier transform is used, only half the total points minus 1 (for the 0) are used
    freqx = np.linspace(0, pointsPerSecond * totalPoints, totalPoints / 2 + 1)

    # convert the result of the FT from points (x= real number, y= imaginary number) to absolute values 
    # by doing sqrt{ a^2 + b^2 } for each point
    fy = abs(f)

    # plot the Fourier Transform
    # use the frequencies on the x-axis
    # use the absolute values of the Fourier Transform on the y-axis
    frequencies.append([freqx, fy])

    # find the highest frequency
    # normalize the found index by multiplying it by the frequency (Hz) 
    # and 2 (since only the real part is taken)
    maxFreq = fy.max()
    highestFreq = np.argmax(fy) * pointsPerSecond * 2
    highestFrequencies.append(highestFreq)

# plot a graph about all the magnitudes and one about all the frequencies
plot(magnitudes, "Magnitudes over time per station", "Time (s)", "Displacement (microns)")
plot(frequencies, "Frequencies per station", "Frequency", "Amplitude (energy of the frequency)")

# print the average frequency from all the measurements
averageHighestFrequency = sum(highestFrequencies) / len(highestFrequencies)
print("Average frequency: " + str(round(averageHighestFrequency, 2)) + "HZ")