from aesCryptHandler import *

aesHandler = AesCryptHandler("super_secrit_master_password")

'''

#specifie destination and source
# standart encryption
aesHandler.encryptFile("test.mp4", "encrypted/test.mp4.aes")

# standart decryption
aesHandler.decryptFile("encrypted/test.mp4.aes", "decrypted/test.mp4")
'''


'''
# specify just source
# standart encryption
aesHandler.encryptFile("test.mp4")

# standart decryption
aesHandler.decryptFile("encrypted/test.mp4.aes")

'''

'''
# delete after encryption / decryption
# standart encryption with deleting source
aesHandler.encryptFile("test.mp4", delete_source=True)

# standart decryption with deleting source
aesHandler.decryptFile("encrypted/test.mp4.aes", delete_source=True)
'''
