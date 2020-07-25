
import data
from PyQt5 import QtCore, QtGui, QtWidgets
import client
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QScrollArea, QGridLayout, QGroupBox, QLabel, QFormLayout

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)



class Ui_DialogAssets(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(data.orderResolution[0]-300, data.orderResolution[1])
        Dialog.setWindowIcon(QtGui.QIcon('bgicon.ico'))
        MainLayout = QGridLayout(Dialog)
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox("")

        if data.mode != "Dark":
            oImage = QImage("background1.jpg")
            sImage = oImage.scaled(QSize(data.orderResolution[0], data.orderResolution[1]))
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sImage))
            Dialog.setPalette(palette)

        else:

            oImage = QImage("background2.jpg")
            sImage = oImage.scaled(QSize(data.orderResolution[0], data.orderResolution[1]))
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sImage))
            Dialog.setPalette(palette)
            # THIS SETS GIF AS A BACKGROUND
            # self.load = QtWidgets.QLabel(Dialog)
            # self.load.setGeometry(0,
            #                       0,
            #                       data.orderResolution[0],
            #                       data.orderResolution[1])
            #
            # self.load.setStyleSheet("QLabel  { text-align: center;};")
            # if data.mode != "Dark":
            #     movie = QtGui.QMovie("giphy1.gif")
            # else:
            #     movie = QtGui.QMovie("giphy1.gif")
            # self.load.setMovie(movie)
            # movie.start()


        user_assets = client.my_assets(data.username, data.password)
       # print("user assetss", user_assets)
        font_ = QtGui.QFont("Times", 20)
        for asset in user_assets:
            if int(asset[2]) <= 0:           # TODO UNCOMMENT
                continue
            thisasset = QLabel()
            thisasset.setFont(font_)
            sign = asset[1] + "\t\t"
            sign += "Amount: " + str(int(asset[2]))
            thisasset.setText(sign)
            self.formLayout.addRow(thisasset)




        self.groupBox.setLayout(self.formLayout)
        scroll = QScrollArea()
        scroll.setWidget(self.groupBox)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color:transparent;")
        MainLayout.addWidget(scroll, 0, 1)


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "My assets"))



