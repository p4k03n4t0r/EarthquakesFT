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