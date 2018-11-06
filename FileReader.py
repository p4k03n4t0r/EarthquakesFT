from itertools import groupby
import os

# get all files from the provided folder name grouped per station
# only the North-South and East-West files of a station are returned
# the Vertical file is ignored
def getFilesPerStation(folder):
    files = os.listdir(folder)

    filesWithPath = []
    # add the folder to the path of each file
    for file in files:
        filesWithPath.append(folder + "/" + file)

    # we group the files based on the first 11 characters (indicating state and station)
    # example: Data/IU.KBS
    groupedFiles = [list(g) for k, g in groupby(filesWithPath, key=lambda x: x[:(len(folder) + 11)])]

    # we are only interested in the North-South (BHN or BH1) and East-West (BHE or BH2) files of each station
    # the Vertical filez (BHZ) are ignored
    filteredGroupedFiles = []
    for fileGroup in groupedFiles:
        fileBHN = [file for file in fileGroup if "BHN" in file or "BH1" in file]
        fileBHE = [file for file in fileGroup if "BHE" in file or "BH2" in file]
        # if this file group has both a BHN and BHE seismogram add them
        if(len(fileBHN) > 0 and len(fileBHE) > 0):
            filteredGroupedFiles.append([fileBHN[0], fileBHE[0]])

    return filteredGroupedFiles

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

# retrieve the current existing directories
def getDataDirectories():
    files = os.listdir(os.getcwd())
    directories = []
    for f in files:
        # ignore files (they contain a dot) and python folder (they contain underscores)
        if("." not in f and "_" not in f):
            directories.append(f)
    return directories