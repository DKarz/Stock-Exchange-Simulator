
import data
from PyQt5 import QtCore, QtGui, QtWidgets
import client
from PyQt5.QtWidgets import QVBoxLayout, QLabel

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
from PyQt5.QtCore import QThread, Qt, pyqtSignal
import time
class MyThread(QThread):
    # Create a counter thread
    change_value = pyqtSignal(int)
    timeToSleep = pyqtSignal(int)
    def run(self):
        try:
            cnt = 0
            while True:
                #cnt += 1
                #print(cnt)
                time.sleep(self.timeToSleep)
                self.change_value.emit(cnt)
        except:
            print("MyThread error")

class Error(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(data.orderResolution[0]/4, data.orderResolution[1]/6)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        Dialog.setWindowFlags(flags)
        MainLayout = QVBoxLayout(Dialog)
        MainLayout.addWidget(QLabel("Trying to connect to server"))
        self.load = QLabel()
        self.load.setAlignment(Qt.AlignCenter)
        if data.mode != "Dark":
            movie = QtGui.QMovie("loading.gif")
        else:
            movie = QtGui.QMovie("loadingDark.gif")
        self.load.setMovie(movie)
        movie.start()
        MainLayout.addWidget(self.load)

        self.thread = MyThread()  # time
        self.thread.timeToSleep = 5
        self.thread.change_value.connect(lambda: setProgressVal())
        self.thread.start()


        def setProgressVal():
            try:
                r = client.update()      #check if the server is alive
                Dialog.close()
                data.error =False
            except:
                pass



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CONFIRM"))



