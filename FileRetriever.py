from ftplib import FTP
import os

# retrieve the data from Wilber 3: http://ds.iris.edu/wilber3
def retrieveWilberData(directory, outputDirectory):
    # create output directory if it doesn't exist yet
    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    # create a ftp connection with the Wilber ftp server
    ftp = FTP("ds.iris.edu")
    ftp.login() 
    wilberDirectory = "pub/userdata/wilber/"

    # go to the provided directory
    ftp.cwd(wilberDirectory + directory)
    filenames = ftp.nlst()

    # download all files
    for filename in filenames:
        local_filename = os.path.join(os.getcwd() + "/" + outputDirectory, filename)
        print("Downloading " + filename)
        file = open(local_filename, "wb")
        ftp.retrbinary("RETR "+ filename, file.write)
        file.close()

    ftp.quit()