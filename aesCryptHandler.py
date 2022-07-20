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


class AesHelper:
    def __init__(self):
        self.encryption = True
        self.target = ""
        self.dest = os.path.join(os.getcwd(), "decrypted")
        self.password = ""

    def execute(self):
        self.handler = AesCryptHandler(self.password)
        if self.encryption:

            if os.path.isdir(self.dest):
                self.handler.encryptFile(
                    self.target, os.path.join(self.dest, ntpath.basename(self.target) + ".aes"))
            else:
                if ".aes" not in self.dest:
                    self.dest += ".aes"
                print("saving encrypted file to : " + str(os.path.join(os.getcwd(),
                                                                       "encrypted")) + "  As -> " + str(self.dest))
                self.handler.encryptFile(
                    self.target, os.path.join(os.path.join(os.getcwd(),
                                                           "encrypted"), self.dest))
        else:
            # decryption
            self.handler.decryptFile(self.target, self.dest)


aes_helper = AesHelper()
try:
    if sys.argv[1] == '-e':
        # encrype
        aes_helper.encryption = True
    if "-d" == sys.argv[1]:
        # decrypt
        aes_helper.encryption = False
    if "-p" == sys.argv[2]:
        # password
        aes_helper.password = sys.argv[3]
    if "-f" == sys.argv[4]:
        # password
        aes_helper.target = sys.argv[5]
    if "-o" == sys.argv[6]:
        # password
        aes_helper.dest = sys.argv[7]

    aes_helper.execute()
except:
    print("please give all required params here is an example !")
    print(r'>aesCryptHandler.py" -e -p 12345678 -f somefile.txt -o ./encrypted')


"""
tests :
 

"""
