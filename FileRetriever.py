from ftplib import FTP
import os

# retrieve the contents of this users folder on the Wilber ftp service
def retrieveWilberFolderContent(directory):
    # create a ftp connection with the Wilber ftp server
    ftp = FTP("ds.iris.edu")
    ftp.login() 

    # go to the provided directory
    ftp.cwd("pub/userdata/wilber/" + directory)
    return ftp.nlst()

# retrieve the data from Wilber 3: http://ds.iris.edu/wilber3
def retrieveWilberData(wilberUsername, earthquakeFolder):
    directory = wilberUsername + "/" + earthquakeFolder + "/timeseries_data"
    # create output directory if it doesn't exist yet
    if not os.path.exists(earthquakeFolder):
        os.makedirs(earthquakeFolder)

    # create a ftp connection with the Wilber ftp server
    ftp = FTP("ds.iris.edu")
    ftp.login() 
    wilberDirectory = "pub/userdata/wilber/"

    # go to the provided directory
    ftp.cwd(wilberDirectory + directory)
    filenames = ftp.nlst()

    # download all files
    for filename in filenames:
        local_filename = os.path.join(os.getcwd() + "/" + earthquakeFolder, filename)

        # only download the non existing files
        if not os.path.exists(local_filename):
            print("Downloading " + filename)
            file = open(local_filename, "wb")
            ftp.retrbinary("RETR "+ filename, file.write)
            file.close()
        else:
            print("Skipping " + filename)

    ftp.quit()