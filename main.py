from time import sleep
from threading import Thread
from pickle import LIST
from config import *
from ftplib import FTP
import sys
import os

isActive = False


def threaded_function(ftp_instance):
    while isActive:
        print("running")
        ftp_instance.sendcmd("NOOP")
        sleep(1)


# default params
encrypted_upload = False
recursive = False

try:
    print('Argument List:', str(sys.argv))
    print("encrypted", str(sys.argv[1]))
    print("src", str(sys.argv[2]))

    if str(sys.argv[1]) == "-e":
        print("encryption before upload activated !")
        encrypted_upload = True
    if str(sys.argv[2]) == "-r":
        recursive = True
        print("recursive uploading activated !")
except:
    print("executing without overrifing params !")

print(encrypted_upload)
paths_to_be_uploaded = []
with open(os.path.join(os.getcwd(), "source.txt")) as f:
    paths_to_be_uploaded = f.readlines()

# print source folders that will be uploaded
print("source folders", str(paths_to_be_uploaded))


def send_file_to_server(file_name, ftp_instance):
    file = open(file_name, 'rb')                  # file to send

    ftp_instance.storbinary(os.path.basename(
        file_name), file)     # send the file
    file.close()


# connect to ftp server
with FTP(host=HOST, user=USER, passwd=PASSWORD, timeout=1600) as ftp:
    ftp.encoding = "utf-8"

    isActive = True
    # ftp.login()
    # list of dirs / files on the current path
    ftp.dir()
    ftp.cwd("www/hdx")
    print("new CWD : \n")
    ftp.dir()
    if not "SFT-noENC" in ftp.nlst():
        ftp.mkd("SFT-noENC")
        ftp.dir()
    ftp.cwd("SFT-noENC")
    # sending files
    # send_file_to_server(str("C:\Users\mehdi\Downloads\Video\I get a new Dildo and use it as a Plug 4kPorn.XXX.mp4"), ftp)
    # file to send
    thread = Thread(target=threaded_function, args=(ftp, ))
    thread.start()
    thread.join()

    '''
    file = open("test.mp4",
                'rb')

    ftp.storbinary("test.mp4",
                   file, blocksize=8192, callback=print("done !"))     # send the file
    file.close()
    '''
    file = open("source.txt",
                'rb')

    ftp.storbinary("source.txt",
                   file, blocksize=8192, callback=print("done !"))     # send the file
    file.close()
    ftp.quit()
isActive = False
