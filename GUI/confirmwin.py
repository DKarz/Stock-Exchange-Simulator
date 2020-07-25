
import data
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)



class Ui_DialogCONFIRM(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(data.orderResolution[0]/4, data.orderResolution[1]/6)
        Dialog.setWindowIcon(QtGui.QIcon('iconQ.ico'))
        MainLayout = QVBoxLayout(Dialog)
        MainLayout.addWidget(QLabel("Are sure that you want to cancel this order?"))

        yes = QPushButton("Yes")
        yes.clicked.connect(lambda: YES())
        no = QPushButton("No")
        no.clicked.connect(lambda: NO())
        MainLayout.addWidget(yes)
        MainLayout.addWidget(no)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        def YES():
            data.toDelete = True
            Dialog.close()
        def NO():
            data.toDelete = False
            Dialog.close()




    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CONFIRM"))



