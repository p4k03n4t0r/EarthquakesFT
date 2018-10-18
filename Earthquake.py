import numpy as np
from FileReader import getFilesPerStation, getData, getTotalPoints, getPointsPerSecond
from FrequencyHelper import addWindow, rotate
from GraphPlot import plot, plotDisplacement
from FileRetriever import retrieveWilberData, retrieveFolderContent
import matplotlib.pyplot as plt
from scipy import signal

#urls = ["paul/2018-05-01-mww52-northern-molucca-sea/timeseries_data/", "paul/2018-04-24-mww52-myanmar/timeseries_data/", "paul/2018-06-29-mww52-hawaii/timeseries_data/", "paul/2017-12-29-mww51-near-coast-of-guatemala/timeseries_data/", ""]
urls = retrieveFolderContent("paul")
for url in urls:
    print("Retrieving " + url)
    retrieveWilberData("paul/" + url + "/timeseries_data", url)

    # lists for the magnitudes and frequencies, which can be used to plot the graph
    magnitudes = []
    frequencies = []
    highestFrequencies = []

    filesPerStation = getFilesPerStation(url)
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

        # get the North-South and East-West values from the files
        # make sure the lines stay around 0, so it is properly calibrated
        yNS = signal.detrend(getData(fileNS))
        yEW = signal.detrend(getData(fileEW))

        # plot the displacement, North-Sound on the y-axis and East-West on the x-axis
        #plotDisplacement(yNS, yEW)

        # rotate the points from North-South on Y-axis and East-West on X-axis
        # to maximum amplitude face the Y-axis
        yX, yY = rotate(yNS, yEW)
        #plotDisplacement(yX, yY)

        # use the most displaced axis to calculate the frequency
        # apply a window function to make the data fit for FT
        y = addWindow(yY)

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
    #plot(magnitudes, "Magnitudes over time per station", "Time (s)", "Displacement (microns)")
    #plot(frequencies, "Frequencies per station", "Frequency", "Amplitude (energy of the frequency)")

    # print the average frequency from all the measurements
    averageHighestFrequency = sum(highestFrequencies) / len(highestFrequencies)
    print("Average frequency: " + str(round(averageHighestFrequency, 2)) + "HZ")