This script uploads stuff to your server using sftp it's fast and it has special features such as encryp files before upload upload folders and recreate the tree structure on the server and it uses threads so u can upload many files at the same time.

 - upload file
 - upload multiple files 
 - upload directories recurssivly
 - encrypt files and folders 
 - upload with encryption or without encryption 

 # how to use 
- the first thing to do is to fill `source.txt` by copy past paths you want to upload using ssh (it doesn't matter if the paths are files or directories)

-Then you have to give params to the script or not, the script takes 3 main params `-e` in case you want to encrypt then upload encrypted files only, `-d`  or `-delete-source` if you want to delete the source files after uploading them finaly `-k` or `-keep-encrypted` if you want to keep encrypted files after upload.
if you don't specify any param the defaul behaviour of the script will be upload source files without encryption and without deleting anything !

 using this three params you have interesting conbinations such as :

 ## upload files then delete them
` python ssh.py -d`

## upload encrypted files but keep them in local but delete source instead
` python ssh.py -e -k -d`

 # if u think that this script is badass and u wanna be fren don't forget do donate and send a message ! UWU X>
<img src="https://isthmaroc.com/qrcode.png" data-canonical-src="https://isthmaroc.com/qrcode.png" width="300" height="300" />

