
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import data
import mainWindow
import functions
import client
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QComboBox

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MyThread(QThread):
    try:
        # Create a counter thread
        change_value = pyqtSignal(int)
        timeToSleep = pyqtSignal(int)
        def run(self):
            try:
                cnt = 0
                while True:
                    #cnt += 1
                    #print(cnt)
                    self.change_value.emit(cnt)
                    time.sleep(self.timeToSleep)
            except:
                print("MyThread error")
    except: pass

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        self.x = 403
        self.y = 329
        Dialog.resize(self.x, self.y)
        Dialog.setStyleSheet("background: rgba(210, 210, 210, 255);")
        Dialog.setWindowIcon(QtGui.QIcon('icon1.ico'))
        #MainLayout = QVBoxLayout(Dialog)
        self.L = QGridLayout(Dialog)
        self.uNameLine = QLineEdit()
        self.idLine = QLineEdit()
        self.IPline = QLineEdit()
        self.uPasswordLine = QLineEdit()
        self.signInButton = QPushButton("Sign In")
        self.signInButton.clicked.connect(lambda : self.signingIn(Dialog))
        self.RegBut = QPushButton("Sign Up")
        self.RegBut.clicked.connect(lambda : self.signingUp(Dialog))
        self.L.addWidget(QtWidgets.QLabel("Name"), 0,0)
        self.L.addWidget(self.uNameLine, 0,1)
        self.L.addWidget(QtWidgets.QLabel("IP"), 2, 0)
        self.L.addWidget(self.IPline, 2,1)
        self.L.addWidget(QtWidgets.QLabel("Password"), 3, 0)
        self.L.addWidget(self.uPasswordLine, 3, 1)
        self.IPline.setText(client.IP)
        self.L.addWidget(self.RegBut, 4, 0)
        self.L.addWidget(self.signInButton, 4, 1)
        self.infLabel = QtWidgets.QLabel("                      ")
        self.infLabel.setFixedHeight(15)
        self.L.addWidget(self.infLabel, 5, 1)
        self.uPasswordLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.size = QComboBox()
        self.size.addItem("Small")
        self.size.addItem("Big")
        self.L.addWidget(QtWidgets.QLabel("Window Size"), 6, 0)
        self.L.addWidget(self.size, 6, 1) # [1.14,1.2, 4.5,1.4]


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        # TODO START IT
        '''
        self.thread = MyThread()  # time
        self.thread.timeToSleep = 3600
        self.thread.change_value.connect(lambda: functions.getNews())
        self.thread.start()                                                              
        '''






######################

    def clearWin(self, Dialog):
        for i in reversed(range(self.L.count())):
            self.L.itemAt(i).widget().setParent(None)

        #return
        Dialog.close()




    def signingIn(self, Dialog):


        uName = self.uNameLine.text()
        uPassword = self.uPasswordLine.text()
        ip = self.IPline.text()
        data.username = uName
        data.password = uPassword

        client.IP = ip
        if not client.known_user(uName, uPassword):
            self.infLabel.setText("Wrong login/password")
            return


        if len(data.username)!=0 and len(data.userid)!=0 and len(data.password)!=0 and len( client.IP)!=0 and functions.is_number(data.userid):
            print("start")
            try:
                 data.userid = client.get_id(uName)
                 data.balance = (client.get_balance(uName), "$")
                 if self.size.currentText() == "Big":
                     data.scale = [1.14, 1.2, 4.5, 1.4]
                     data.scale_ = [2.1,1.5,4.3,3]
                 functions.putPersonalData()
                 mainWindow.runGUI()
                 #print("singIn")

            except:
                print("Error while starting app")
                self.clearWin(Dialog)

        else:
            self.infLabel.setText("Error. Try Again!")

        return


    def signingUp(self, Dialog):


        uName = self.uNameLine.text()
        uPassword = self.uPasswordLine.text()
        if client.known_user(uName, False):
            self.infLabel.setText("Cannot use this login!")
            return
        client.register(uName,uPassword)

        ip = self.IPline.text()
        data.username = uName
        data.password = uPassword

        client.IP = ip
        print("4")
        if len(data.username)!=0 and len(data.userid)!=0 and len(data.password)!=0 and len( client.IP)!=0 and functions.is_number(data.userid):
            print("start")
            try:
                data.userid = client.get_id(uName)
                data.balance = (client.get_balance(uName), "$")
                if self.size.currentText() == "Big":
                    data.scale = [1.14, 1.2, 4.5, 1.4]
                    data.scale_ = [2.1, 1.5, 4.3, 3]
                functions.putPersonalData()

                mainWindow.runGUI()
                #print("signUp")
            except:
                print("Error while starting app")
                self.clearWin(Dialog)
        else:
            self.infLabel.setText("Error. Try Again!")

        return

    def closewin(self):
        pass
       # self.thread.terminate()



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "User Verification"))


