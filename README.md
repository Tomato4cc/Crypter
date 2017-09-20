Alternative PES file crypter v1.0. Supports decryption/encryption of PES
EDIT files and zlibbing/unzlibbing of several filetypes either one-by-one
or in larger batches inside a folder.

Usage:
 - Drag-and-Drop the file/folder you want to process and the tool will do
   the rest.
 - Decrypter takes an encrypted PES18 EDIT file. Otherwise the external file
   decrypter18.exe will crash and the tool won't proceed. Still, don't feed
   it invalid data since something might go wrong.
 - Encrypter takes a decrypted PES18 EDIT file, usually one created by using
   the tool's Decrypter function. The tool checks if the header of the file
   is correct and then assumes the rest is fine and tries to encrypt the
   file to produce a valid PES18 EDIT file. Feeding the function invalid
   data will produce an invalid EDIT file.
 - UnZlib takes either a file or a folder. If the input is a folder the 
   function will unzlib every supported file inside that folder and place
   them in the "unzlibbed" folder at the tool's root directory.
 - Zlib takes either a file or a folder. If the input is a folder the 
   function will zlib every supported file inside that folder and place
   them in the "zlibbed" folder at the tool's root directory.
   
Building:
  - .exe releases are built with pyinstaller. The standard build command for
    a release is `pyinstaller -F -w -i icon.ico crypter.py`. Only the .py, 
	the .ico and the **ui** folder are required for building.