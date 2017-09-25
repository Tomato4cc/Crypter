# -*- coding: utf-8 -*-

#Created from a .ui source file by PyQt5 UI code generator 5.7.1
#Manually modified from there to better suit the program
#Not very commented since it's mostly autogenerated UI code
#You'll know what to do if you have experience with PyQT

from PyQt5 import QtCore, QtGui, QtWidgets

#Extend QGroupBox for our drop-down area
class DnDBox(QtWidgets.QGroupBox):
    def __init__(self, type, parent=None):
        super(DnDBox, self).__init__(parent)
        self.setAcceptDrops(True)
    
    #Signal to send on drop
    dropped = QtCore.pyqtSignal(list)
    
    #Define the required events
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls:
            e.setDropAction(QtCore.Qt.CopyAction)
            e.accept()
            l = []
            #Go through the urls in the data. Most likely only one but let's make sure
            for url in e.mimeData().urls():
                l.append(str(url.toLocalFile()))
            self.dropped.emit(l) #Emit the signal once we've got our URLs
        else:
            e.ignore()

class Ui_Crypter(object):
    def setupUi(self, Crypter):
        Crypter.setObjectName("Crypter")
        Crypter.resize(500, 500)
        self.centralWidget = QtWidgets.QWidget(Crypter)
        self.centralWidget.setObjectName("centralWidget")
        self.decryb = DnDBox(self.centralWidget)
        self.decryb.setGeometry(QtCore.QRect(10, 10, 330, 330))
        self.decryb.setTitle("")
        self.decryb.setObjectName("decryb")
        self.decryb.setStyleSheet("border-image: url(img/decrypt.png) 0 0 0 0 stretch stretch;")
        self.encryb = DnDBox(self.centralWidget)
        self.encryb.setGeometry(QtCore.QRect(360, 10, 330, 330))
        self.encryb.setTitle("")
        self.encryb.setObjectName("encryb")
        self.encryb.setStyleSheet("border-image: url(img/encrypt.png) 0 0 0 0 stretch stretch;")
        self.unzlibb = DnDBox(self.centralWidget)
        self.unzlibb.setGeometry(QtCore.QRect(10, 350, 330, 330))
        self.unzlibb.setTitle("")
        self.unzlibb.setObjectName("unzlibb")
        self.unzlibb.setStyleSheet("border-image: url(img/unzlib.png) 0 0 0 0 stretch stretch;")
        self.zlibb = DnDBox(self.centralWidget)
        self.zlibb.setGeometry(QtCore.QRect(360, 350, 330, 330))
        self.zlibb.setTitle("")
        self.zlibb.setObjectName("zlibb")
        self.zlibb.setStyleSheet("border-image: url(img/zlib.png) 0 0 0 0 stretch stretch;")
        Crypter.setCentralWidget(self.centralWidget)
        
        
        self.menuBar = QtWidgets.QMenuBar(Crypter)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menumode = QtWidgets.QMenu(self.menuSettings)
        self.menuSettings.addMenu(self.menumode)
        Crypter.setMenuBar(self.menuBar)
        
        self.exita = QtWidgets.QAction(Crypter)
        self.prefixa = QtWidgets.QAction(Crypter)
        self.prefixa.setCheckable(True)
        self.prefixa.setChecked(True)
        self.backupa = QtWidgets.QAction(Crypter)
        self.backupa.setCheckable(True)
        self.fagroup = QtWidgets.QActionGroup(self.menuBar)
        self.fagroup.addAction(self.prefixa)
        self.fagroup.addAction(self.backupa)
        self.staytopa = QtWidgets.QAction(Crypter)
        self.staytopa.setCheckable(True)
        self.staytopa.setChecked(False)
        
        self.menuFile.addAction(self.exita)
        self.menumode.addAction(self.prefixa)
        self.menumode.addAction(self.backupa)
        self.menuSettings.addAction(self.staytopa)
        
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        
        self.lo = QtWidgets.QGridLayout()
        self.lo.addWidget(self.decryb, 0, 0)
        self.lo.addWidget(self.encryb, 0, 1)
        self.lo.addWidget(self.unzlibb, 1, 0)
        self.lo.addWidget(self.zlibb, 1, 1)
        self.centralWidget.setLayout(self.lo)

        self.retranslateUi(Crypter)
        QtCore.QMetaObject.connectSlotsByName(Crypter)

    def retranslateUi(self, Crypter):
        _translate = QtCore.QCoreApplication.translate
        Crypter.setWindowTitle(_translate("Crypter", "Crypter"))
        self.menuFile.setTitle(_translate("Crypter", "File"))
        self.menuSettings.setTitle(_translate("Crypter", "Settings"))
        self.menumode.setTitle(_translate("Crypter", "Mode"))
        self.exita.setText(_translate("Crypter", "Exit"))
        self.prefixa.setText(_translate("Crypter", "Prefix"))
        self.backupa.setText(_translate("Crypter", "Backup"))
        self.staytopa.setText(_translate("Crypter", "Stay on Top"))

