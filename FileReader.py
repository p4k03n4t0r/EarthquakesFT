import os

# get all files from the provided folder name
def getFiles(folder):
    files = os.listdir(folder)

    filesWithPath = []
    # add the folder to the path of each file
    for file in files:
        filesWithPath.append(folder + "/" + file)
    return filesWithPath

# read a file in the format received from Wilber3: http://ds.iris.edu/wilber3
def getData(file):
    f = open(file, "r") 
    y = []
    # skip some meta data lines
    skipTillLine = 8
    for i, line in enumerate(f):
        if(i <= skipTillLine):
            continue
        # remove line breaks and parse to a number
        y.append(float(line.replace("\n","")))
    
    return y

# get the total points based on the input file in the Wilber3 format
def getTotalPoints(file):
    f = open(file, "r") 
    for i, line in enumerate(f):
        if(i == 3):
            return float(line.replace("# sample_count: ","").replace("\n",""))

# get the points per second based on the input file in the Wilber3 format
def getPointsPerSecond(file):
    f = open(file, "r") 
    for i, line in enumerate(f):
        if(i == 4):
            hz = float(line.replace("# sample_rate_hz: ","").replace("\n",""))
            return 1/hz

# get the start time of the earthquake from the file
# def getStartTime(file):
#     f = open(file, "r") 
#     for i, line in enumerate(f):
#         if(i == 5):
#             return datetime.datetime(line.replace("# start_time: ","").replace("\n","")