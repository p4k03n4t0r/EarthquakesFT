import numpy as np

# get the T value for the provided data
# the provided data is an array with the first value in the array being the x value of that point 
# and the second value the y value
def getTValue(data):
    # the amount of points
    n = len(data)

    # divide the values into two seperate arrays so the average can be calculated
    xValues = []
    yValues = []
    for point in data:
        xValues.append(point[0])
        yValues.append(point[1])
    xAvg = np.average(xValues)
    yAvg = np.average(yValues)

    # calculate the standerd deviation of the sample
    sM = 0
    sF = 0
    for point in data:
        sM = sM + np.square(point[0] - xAvg)
        sF = sF + np.square(point[1] - yAvg)
    sM = np.sqrt(sM/(n-1))
    sF = np.sqrt(sF/(n-1))

    # calculate the R value
    r = 0
    for point in data:
        r += ((point[0] - xAvg) / sM) * ((point[1] - yAvg) / sF)
    r *= (1/(n-1))

    # calculate the T value
    t = r * np.sqrt((n-2)/(1-np.square(r)))
    
    return t