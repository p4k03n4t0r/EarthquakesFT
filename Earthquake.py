import numpy as np
from FileReader import getFilesPerStation, getData, getTotalPoints, getPointsPerSecond
from FrequencyHelper import addWindow, rotate
from GraphPlot import plot, plotDisplacement, plotMagnitudeFrequency
from FileRetriever import retrieveWilberData, retrieveWilberFolderContent
from scipy import signal
from StatisticsHelper import getTValue

# retrieve the earthquakes available for this user from Wilber 3
username = "paul"
earthquakeFolders = retrieveWilberFolderContent(username)

frequenciesForMwMagnitude = []
frequenciesForMbMagnitude = []
for earthquakeFolder in earthquakeFolders:
    try:   
        print("Retrieving " + earthquakeFolder)
        retrieveWilberData(username, earthquakeFolder)

        # lists for the magnitudes and frequencies, which can be used to plot the graph
        magnitudes = []
        frequencies = []
        highestFrequencies = []

        filesPerStation = getFilesPerStation(earthquakeFolder)
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

        # calculate the average frequency
        averageHighestFrequency = sum(highestFrequencies) / len(highestFrequencies)

        # print the average frequency from all the measurements
        print(earthquakeFolder + ": " + str(round(averageHighestFrequency, 2)) + "Hz")

        # retrieve the magnitude of the earthquake (earthquakeFolder contains the name of the earthquake)
        # Example: 2007-08-15-mw81-near-coast-of-peru (magnitudeScale: mw and magnitude: 8.1)
        earthquakeMagnitude = earthquakeFolder.split("-")[3]
        magnitudeScale = earthquakeMagnitude[:2]
        magnitude = float(earthquakeMagnitude[2:4])/10

        # depending on the magnitude scale, divide the earthquake into the right magnitude scale
        if(magnitudeScale == "mw" and magnitude >= 5.5):
            frequenciesForMwMagnitude.append([magnitude,averageHighestFrequency])
        elif(magnitudeScale == "mb" and magnitude >= 3 and magnitude <= 5):
            frequenciesForMbMagnitude.append([magnitude,averageHighestFrequency])
        else:
            print("Unknown magnitude scale: " + magnitudeScale)
    except:
        print("Unexpected error for file " + earthquakeFolder)

# plot the frequencies and magnitudes in a scatterplot so there can be searched for a relation between them
plotMagnitudeFrequency(frequenciesForMbMagnitude, "Mb")
print("T value for Mb scale: " + str(getTValue(frequenciesForMbMagnitude)))
plotMagnitudeFrequency(frequenciesForMwMagnitude, "Mw")
print("T value for Mw scale: " + str(getTValue(frequenciesForMwMagnitude)))