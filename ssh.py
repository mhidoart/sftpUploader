import paramiko
import os
from config import *


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


class SSHHandler():
    def __init__(self, sshHost, sshPort,  sshUsername, sshPassword, sshTimeout):
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.s.connect(sshHost, sshPort, username=sshUsername,
                       password=sshPassword, timeout=sshTimeout)
        self.sftp = self.s.open_sftp()

    def putFile(self, source, dest, callback):
        try:
            return self.sftp.put(source, dest, callback)
        except:
            print("can't upload file !")

    def removeFileFromHost(self, path):
        try:
            return self.sftp.remove(path)
        except:
            print("file can't be removed !")
            return None

    def closeConnection(self):
        self.sftp.close()


def someFunction(arr):
    print(arr)


handler = SSHHandler(HOST, 22, USER, PASSWORD, 4)
size = handler.putFile(
    "test.mp4", 'www/hdx/SFT-noENC/test.mp4', someFunction("ttt"))
print("Size : " + str(size))


handler.closeConnection()
