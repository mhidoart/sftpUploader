from fileinput import filename
from posixpath import dirname
import paramiko
import os
import sys
from config import *
import ntpath
from aesCryptHandler import *


def advancement(transfered, total):
    print("transfered " + str(transfered))
    print("Total: " + str(total))


'''
s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect(HOST, 22, username=USER, password=PASSWORD, timeout=4)

sftp = s.open_sftp()

stdin, stdout, stderr = s.exec_command("ls")
print(stdout.readlines())


sftp.put(os.path.join(os.getcwd(), 'source.txt'),
         'www/hdx/SFT-noENC/resource.txt')
print('--------------------------------')
print(str(sftp.put(os.path.join(os.getcwd(), 'test.mp4'),
                   'www/hdx/SFT-noENC/test.mp4', advancement(int, int))))

sftp.close()
'''


class SSHHandler:
    def __init__(self, sshHost, sshPort,  sshUsername, sshPassword, sshTimeout, master_encryption_password="super secret pass, comme on change it u dumb ass",
                 encrypted_upload=False, keep_encrypted=False, deleteSource=False):
        self.encrypted_upload = encrypted_upload
        self.keep_encrypted = keep_encrypted
        self.deleteSource = deleteSource
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.s.connect(sshHost, sshPort, username=sshUsername,
                       password=sshPassword, timeout=sshTimeout)
        self.sftp = self.s.open_sftp()
        self.aesHandler = AesCryptHandler(master_encryption_password)

    def putFile(self, source, dest, callback):
        try:
            return self.sftp.put(source, dest, callback)
        except:
            print("can't upload file !")

    def createDirectory(self, path):
        try:
            return self.sftp.mkdir(path)
        except:
            print("can't create Folder !")

    def removeFileFromHost(self, path):
        try:
            return self.sftp.remove(path)
        except:
            print("file can't be removed !")
            return None

    def closeConnection(self):
        self.sftp.close()

    def getPaths(self, source):
        paths = os.listdir(source)
        paths = [os.path.join(source, s.strip()) for s in paths]
        # normalising paths
        paths = [os.path.normpath(s) for s in paths]
        return paths

    def deleteFileFromLocal(self, path, verbose=False):
        try:
            if verbose:
                print("deleting local directory : " + str(path))
            os.remove(path)
            return True
        except:
            if verbose:
                print("failed to remove directory from local : " + str(path))
            return False

    def uplodFiles(self, listPaths, index, target):
        if index >= len(listPaths):
            print("Done: uploading directory : " + target)
        else:
            if os.path.isdir(listPaths[index]):
                if target == "":
                    target = TARGET_PATH
                # recurssive call
                self.createDirectory(
                    target + ntpath.basename(listPaths[index]))
                dir = target + ntpath.basename(listPaths[index]) + "/"
                #print("new target added : " + dir + " start upload with new list : " +str(self.getPaths(listPaths[index])))
                self.uplodFiles(self.getPaths(listPaths[index]), 0, dir)
            else:
                # upload file
                size = -1
                # if encryption is activated
                if self.encrypted_upload:
                    if self.deleteSource:
                        listPaths[index] = self.aesHandler.encryptFile(
                            listPaths[index], delete_source=True)
                    else:

                        listPaths[index] = self.aesHandler.encryptFile(
                            listPaths[index])

                # extract filename with extention from the source file
                filename = ntpath.basename(listPaths[index])
                print("start uploading .. " + filename +
                      " to: " + TARGET_PATH + target + filename)
                if target == "":
                    self.putFile(listPaths[index], TARGET_PATH + target +
                                 filename,  someFunction("start uploading .. " + filename))
                else:

                    self.putFile(listPaths[index], target +
                                 filename,  someFunction("start uploading .. " + filename))
                # keep encrypted files or not
                    if not self.keep_encrypted:
                        self.deleteFileFromLocal(listPaths[index], True)

                print(" done uploading : " +
                      listPaths[index] + " to: " + target + "\n Details: " + str(size))
                self.uplodFiles(listPaths, index+1, target)


def someFunction(arr):
    print(arr)


# default params
encrypted_upload = False
keep_encrypted = False
deleteSource = False

try:
    if '-e' in sys.argv:
        print("encryption before upload activated !")
        encrypted_upload = True
    if "-keep-encrypted" in sys.argv or "-k" in sys.argv:
        keep_encrypted = True
        print("keep_encrypted  activated !")
    if "-delete-source" in sys.argv or "-d" in sys.argv:
        deleteSource = True
except:
    print("executing without overrifing params !")


handler = SSHHandler(HOST, 22, USER, PASSWORD, 4,
                     MASTER_ENCRYPTION_PASSWORD,
                     encrypted_upload, keep_encrypted, deleteSource)
# creating the parent node that will host the fils later
handler.createDirectory(TARGET_PATH)


'''
# upload single filer
size = handler.putFile(
    "test.mp4", 'www/hdx/SFT-noENC/test.mp4', someFunction("ttt"))
print("Size : " + str(size))
'''


# reading ressource file
paths = []
with open("source.txt") as f:
    paths = [s.strip() for s in f.readlines()]
    # normalising paths
    paths = [os.path.normpath(s) for s in paths]


# for loop on each file
handler.uplodFiles(paths, 0, "")


# uplodFiles(paths, 0)
handler.closeConnection()
