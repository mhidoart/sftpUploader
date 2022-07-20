import pyAesCrypt
import os
import ntpath
import sys


class AesCryptHandler:
    def __init__(self, masterPassword):
        self.masterPassword = masterPassword
        # creating workspace for encr/decryption
        self.encryption_default_path = os.path.join(os.getcwd(), "encrypted")
        self.decryption_default_path = os.path.join(os.getcwd(), "decrypted")
        if not os.path.exists(self.encryption_default_path):
            os.makedirs(self.encryption_default_path)
        if not os.path.exists(self.decryption_default_path):
            os.makedirs(self.decryption_default_path)

    def encryptFile(self, source, dest="", passw="", delete_source=False):
        try:
            # if no password was specified the default password s the one passed to the constructor
            if passw == "":
                passw = self.masterPassword
            # in case of no destination is specified we use the default workspace
            if(dest == ""):
                dest = os.path.join(
                    self.encryption_default_path, ntpath.basename(source))
            if not str(dest).endswith(".aes"):
                dest = dest + ".aes"
            pyAesCrypt.encryptFile(source, dest, passw)

            # delete source after encryption
            if delete_source == True:
                os.remove(source)
            return dest
        except:
            print("error encrypting -> ", source)
            return "None"

    def decryptFile(self, source, dest="", passw="", delete_source=False):
        try:
            # if no password was specified the default password s the one passed to the constructor
            if passw == "":
                passw = self.masterPassword
            if(dest == ""):
                dest = os.path.join(
                    self.decryption_default_path, str(ntpath.basename(source)).replace(".aes", ""))
            pyAesCrypt.decryptFile(source, dest, passw)
            # delete source after decryption
            if delete_source == True:
                os.remove(source)
            return dest
        except:
            print("error decrypting -> ", source)
            return "None"


try:
    if sys.argv[1] == '-e':
        # encrype
        print("encrypt option")
    if "-d" == sys.argv[1]:
        # decrypt
        print("decrypt")
    if "-p" == sys.argv[2]:
        # password
        print(str(sys.argv[3]))
    if "-f" == sys.argv[4]:
        # password
        print(str(sys.argv[5]))
except:
    print("please give params to the script ! ")

handler = AesCryptHandler("")
