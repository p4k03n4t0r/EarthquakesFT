import numpy as np
from FileReader import getFiles, getData, getTotalPoints, getPointsPerSecond
from GraphPlot import plot
from FileRetriever import retrieveWilberData
from scipy import signal

# he folder in which the earthquake data can be found
folder = "Data"
#retrieveWilberData("paul/2018-09-15-mb42-adriatic-sea-2/timeseries_data/", folder)

# lists for the magnitudes and frequencies, which can be used to plot the graph
magnitudes = []
frequencies = []
highestFrequencies = []

for file in getFiles(folder):
    # simulate an amount of points based on the files parameters
    totalPoints = getTotalPoints(file)
    pointsPerSecond = getPointsPerSecond(file)

    # get the magnitude from the file
    x = np.linspace(0, pointsPerSecond * totalPoints, totalPoints)
    y = getData(file)

    # make sure the line stays around 0 (it is properly calibrated)
    y = signal.detrend(y)

    # use a window function on the data to make the data fit
    windowFunction = np.bartlett(totalPoints)
    for i, windowFactor in enumerate(windowFunction):
        y[i] = y[i] * windowFactor

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