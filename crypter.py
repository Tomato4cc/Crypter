#Some kind of an all-in-one tool for a handful of PES file formats.
#So far can encrypt/decrypt EDIT files and zlib/unzlib texture .dds files
#either one at a time or in bulk.
#More features to be added probably soon maybe.

import os
import shutil
import sys
import subprocess
import zlib
import struct

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui.ui import Ui_Crypter

class Crypter(QMainWindow, Ui_Crypter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('img/icon.png'))
        
        #Connect signals
        self.decryb.dropped.connect(self.decrypt)
        self.encryb.dropped.connect(self.encrypt)
        self.unzlibb.dropped.connect(self.unzlib)
        self.zlibb.dropped.connect(self.zlib)
        self.staytopa.toggled.connect(self.staytop)
        self.exita.triggered.connect(self.closef)
        
        self.root = os.path.dirname(os.path.realpath(__file__)) #Store the script root dir
        self.temp = os.path.join(self.root, 'temp') #Store the temp dir
        self.unzl = os.path.join(self.root, 'unzlibbed') #Store the dir for batch unzlibbed files
        self.zl = os.path.join(self.root, 'zlibbed') #Store the dir for batch zlibbed files
    
    #Decrypt an editfile
    def decrypt(self, urll):
        for url in urll:
            if(os.path.isfile(url)):
                os.makedirs(self.temp, exist_ok=True) #Make temp directory since it's needed
                #Attempt to decrypt the file
                subprocess.call([os.path.join(self.root, 'lib', 'decrypter18.exe'), url, self.temp])
                #Very ugly way of checking if all components exist but it'll do for now
                if(os.path.isfile(os.path.join(self.temp, 'description.dat')) and os.path.isfile(os.path.join(self.temp, 'header.dat')) and os.path.isfile(os.path.join(self.temp, 'encryptHeader.dat')) and os.path.isfile(os.path.join(self.temp, 'version.txt')) and os.path.isfile(os.path.join(self.temp, 'logo.png')) and os.path.isfile(os.path.join(self.temp, 'data.dat'))):
                    fname = os.path.basename(url) #Get filename from url
                    #Open destination file for writing
                    o = open(os.path.join(self.root, "decrypted_" + fname), 'wb')
                    #Open description.dat for reading
                    rdesc = open(os.path.join(self.temp, "description.dat"), 'rb')
                    o.write(rdesc.read()) #Write desc into decrypted file
                    rdesc.close()
                    
                    #Open header.dat for reading
                    rhead = open(os.path.join(self.temp, "header.dat"), 'rb')
                    o.write(rhead.read()) #Write head into decrypted file
                    rhead.close()
                    
                    #Open encryptionHeader.dat for reading
                    enchead = open(os.path.join(self.temp, "encryptHeader.dat"), 'rb')
                    o.write(enchead.read()) #Write encryption header into decrypted file
                    enchead.close()
                    
                    #Open version.txt for reading
                    vtext = open(os.path.join(self.temp, "version.txt"), 'rb')
                    o.write(vtext.read()) #Write version string into decrypted file
                    vtext.close()
                    
                    #Open logo.png for reading
                    logo = open(os.path.join(self.temp, "logo.png"), 'rb')
                    o.write(logo.read()) #Write logo into decrypted file
                    logo.close()
                    
                    #Open data.dat for reading
                    data = open(os.path.join(self.temp, "data.dat"), 'rb')
                    o.write(data.read()) #Write data into decrypted file
                    data.close()
                    
                    #All done here, run cleanup
                    o.close()
                    #Remove temp directory
                    shutil.rmtree(self.temp, ignore_errors=True)

    #Encrypt an editfile
    def encrypt(self, urll):
        for url in urll:
            if(os.path.isfile(url)):
                b = open(url, 'rb') #Open file for reading
                #head = b.read(9).decode('utf-8') #Read "header" from file
                #Check if file at least starts correctly.
                if(b):
                    _HEADL = 208 #Header length
                    _ENCHL = 320 #Encryption header length
                    
                    #Read other sizes from the header
                    b.seek(384) #Skip Description
                    b.seek(64, 1) #Skip mystery data in header
                    _DATAL = struct.unpack('<I', b.read(4))[0]
                    _LOGOL = struct.unpack('<I', b.read(4))[0]
                    _DESCL = struct.unpack('<I', b.read(4))[0]
                    _VERSL = struct.unpack('<I', b.read(4))[0]*2
                    
                    fname = os.path.basename(url) #Get filename from url
                        
                    os.makedirs(self.temp, exist_ok=True) #Make temp directory since it's needed
                    b.seek(0) #Get back to the beginning of the source file
                    
                    #Open description.dat for writing
                    o = open(os.path.join(self.temp, 'description.dat'), 'wb')
                    o.write(b.read(_DESCL)) #Write description into file
                    o.close()
                    
                    #Open header.dat for writing
                    o = open(os.path.join(self.temp, 'header.dat'), 'wb')
                    o.write(b.read(_HEADL)) #Write header into file
                    o.close()
                    
                    #Open encryptHeader.dat for writing
                    o = open(os.path.join(self.temp, 'encryptHeader.dat'), 'wb')
                    o.write(b.read(_ENCHL)) #Write encrypt header into file
                    o.close()
                    
                    #Open version.txt for writing
                    o = open(os.path.join(self.temp, 'version.txt'), 'wb')
                    o.write(b.read(_VERSL)) #Write version string into file
                    o.close()
                    
                    #Open logo.png for writing
                    o = open(os.path.join(self.temp, 'logo.png'), 'wb')
                    o.write(b.read(_LOGOL)) #Write logo into file
                    o.close()
                    
                    #Open data.dat for writing
                    o = open(os.path.join(self.temp, 'data.dat'), 'wb')
                    o.write(b.read(_DATAL)) #Write data into file
                    o.close()
                    
                    #All done, run cleanup
                    b.close()
                    #Attempt to encrypt the file
                    subprocess.call([os.path.join(self.root, 'lib', 'encrypter18.exe'), self.temp, os.path.join(self.root, "encrypted_" + fname)])
                    #Remove temp directory
                    shutil.rmtree(self.temp, ignore_errors=True)
                    
    #Unzlib a file
    def unzlib(self, urll):
        for url in urll:
            if(os.path.isfile(url)):
                o = open(url, 'rb')
                if(os.stat(url).st_size > 0): #Make sure there's something to read
                    o.seek(3, 0) #Seek to the header
                    head = o.read(5) #Read the header
                    #Check to make sure the file is zlibbed
                    if(head == b'WESYS'):
                        o.seek(16,0) #Skip the file header and the PES header
                        dat = o.read() #Read the actual compressed data
                        #Use .backup system if needed
                        if(self.backupa.isChecked()):
                            #Open .backup for writing
                            bak = open(os.path.join(os.path.dirname(url), os.path.basename(url) + ".backup"), 'wb')
                            o.seek(0) #Go back to the start of the original file
                            bak.write(o.read()) #Dump original file into .backup
                            bak.close()
                            o.close()
                            
                            #Then write unzlibbed data into original file
                            decomp = open(url, 'wb')
                        #Otherwise use prefix system
                        else:
                            decomp = open(os.path.join(os.path.dirname(url), "unzlibbed_" + os.path.basename(url)), 'wb')
                            o.close()
                        
                        cdat = zlib.decompress(dat, 32) #Decompress the data
                        decomp.write(cdat)
                        decomp.flush()
                        decomp.close()
                    else:
                        o.close()
            #Also support batch unzlibbing if the dragged object is a dir
            elif(os.path.isdir(url)):
                exts = ['.dds', '.bin', '.xml', '.mtl', '.lua'] #List of filetypes to process
                os.makedirs(self.unzl, exist_ok=True) #Make temp directory since it's needed
                for r, d, f in os.walk(url): #Go through the whole folder
                    for file in f:
                        if(any(e in file.lower() for e in exts)): #Match the file extensions list to current file
                            o = open(os.path.join(r, file), 'rb')
                            if(os.stat(os.path.join(r, file)).st_size > 0): #Make sure there's something to read
                                o.seek(3, 0) #Seek to the header
                                head = o.read(5) #Read the header
                                if(head == b'WESYS'):
                                    o.seek(16,0) #Skip the file header and the PES header
                                    dat = o.read() #Read the actual compressed data
                                    decomp = open(os.path.join(self.unzl, file), 'wb')
                                    cdat = zlib.decompress(dat, 32) #Decompress the data
                                    decomp.write(cdat) #Write decompressed data
                                    decomp.flush()
                                    decomp.close()
                                o.close()
    
    #Zlib a file
    def zlib(self, urll):
        for url in urll:
            if(os.path.isfile(url)):
                o = open(os.path.join(url), 'rb') #Open file for reading
                head = o.read(8) #Store the header of the file
                o.seek(0,0) #Back to the start
                dat = o.read() #Store the entire file
                o.close()
                h = struct.unpack('2I', head) #Unpack the header for checking
                
                #Magic check to make sure the file is not already zlibbed.
                #PES zlibbed files always start with 0x000101 WESYS
                if(h[0] != 1459683584 and h[1] != 1398362949):
                    #File is not zlibbed yet, get to work
                    #Use backup system if needed
                    if(self.backupa.isChecked()):
                        #Open .backup for writing
                        bak = open(os.path.join(os.path.dirname(url), os.path.basename(url) + ".backup"), 'wb')
                        bak.write(dat) #Dump original file into .backup
                        bak.close()
                        
                        #Then write unzlibbed data into original file
                        comp = open(url, 'wb')
                    #Otherwise use prefix system
                    else:
                        comp = open(os.path.join(os.path.dirname(url), "zlibbed_" + os.path.basename(url)), 'wb')
                    
                    cdat = zlib.compress(dat, 9) #Compress the whole file with the highest level of compression
                    #Write the compressed data in the PES special format.
                    #Start with the 0x000101 WESYS, then length of the compressed data, then length of the original data
                    comp.write(struct.pack("4I",0x57010100, 0x53595345, len(cdat), len(dat)))
                    comp.write(cdat)
                    comp.flush()
                    comp.close()
                #Also support batch zlibbing if the dragged object is a dir
            elif(os.path.isdir(url)):
                exts = ['.dds'] #List of filetypes to process
                os.makedirs(self.zl, exist_ok=True) #Make temp directory since it's needed
                for r, d, f in os.walk(url): #Go through the whole folder
                    for file in f:
                        if(any(e in file for e in exts)): #Check if current file matches the filetype list
                            o = open(os.path.join(r, file), 'rb')
                            head = o.read(8) #Store the header of the file
                            o.seek(0,0) #Back to the start
                            dat = o.read() #Store the entire file
                            o.close()
                            h = struct.unpack('2I', head) #Unpack the header for checking
                            
                            #Magic check to make sure the file is not already zlibbed.
                            #PES zlibbed files always start with 0x000101 WESYS
                            if(h[0] != 1459683584 and h[1] != 1398362949): 
                                #File is not zlibbed yet, get to work
                                comp = open(os.path.join(self.zl, file), 'wb')
                                cdat = zlib.compress(dat, 9) #Compress the whole file with the highest level of compression
                                #Write the compressed data in the PES special format.
                                #Start with the 0x000101 WESYS, then length of the compressed data, then length of the original data
                                comp.write(struct.pack("4I",0x57010100, 0x53595345, len(cdat), len(dat)))
                                comp.write(cdat) #Write compressed data
                                comp.flush()
                                comp.close()
    
    #Make the window stay on top if required
    def staytop(self, checked):
        if(checked == True):
            #Set the WindowStaysOnTopHint window flag
            self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
            self.show() #Redraw the window to apply the changes
        else:
            print("Unchecked")
            #Unset the WindowStaysOnTopHint window flag
            self.setWindowFlags(self.windowFlags() & ~Qt.CustomizeWindowHint & ~Qt.WindowStaysOnTopHint)
            self.show() #Redraw the window to apply the changes
    
    #Simply end the process if Exit is clicked
    def closef(self):
        sys.exit(0)
    
if __name__ == "__main__":
    p = QApplication(sys.argv)
    w = Crypter()
    w.show()
    sys.exit(p.exec_())