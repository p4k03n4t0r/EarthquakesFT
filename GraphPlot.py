import matplotlib.pyplot as plt

# create a plot based on the provided data, graph name and axis labels
def plot(data, graphName, xlabel, ylabel):
    for coordinates in data:
        plt.plot(coordinates[0], coordinates[1])

    plt.title(graphName)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()

# plot the displacement based on the North-South and East-West displacement
def plotDisplacement(yNS, yEW):
    plt.plot(yNS, yEW)
    plt.title("Displacement")
    plt.xlabel("East-West displacement (microns)")
    plt.ylabel("North-South displacement (microns)")
    plt.grid()
    plt.show()

# plot the provided data in a histogram
def plotHistogram(data, totalBins):
    plt.hist(data, bins=totalBins)
    plt.show()