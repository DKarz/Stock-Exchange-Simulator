
import data
import functions as func
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt
import client
from time import time
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QComboBox

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)



class Ui_DialogOrder(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(data.orderResolution[0], data.orderResolution[1])

        MainLayout = QVBoxLayout(Dialog)
        searchLine = QHBoxLayout()
        self.sLine = QtWidgets.QLineEdit()
        if data.autocomplete != "No filter":
            self.sLine.setText(data.autocomplete)
        Dialog.setWindowIcon(QtGui.QIcon('icon1.ico'))
        sBut = QPushButton("GO")
        sBut.clicked.connect(lambda: runEngine())
        searchLine.addWidget(self.sLine)
        searchLine.addWidget(sBut)
        filter = QHBoxLayout()
        self.ordertype = QComboBox()
        self.ordertype.addItem("Limit")
        self.ordertype.addItem("FillorKill")
        filter.addWidget(self.ordertype)
        self.ordertype.currentIndexChanged.connect(self.prdChanged, self.ordertype.currentIndex())
        filter.addWidget(QLabel("Amount: "))
        amount = QtWidgets.QLineEdit()
        #amount.setInputMask("999999")

        amount.setText(data.acAmount)
        filter.addWidget(amount)

        filter.addWidget(QLabel("Price: "))
        self.price = QtWidgets.QLineEdit()
        self.price.setText(data.acPrice)
        filter.addWidget(self.price)
        filter.addWidget(QLabel("$"))
        statusLabel = QLabel("\n")
        statusLabel.setAlignment(Qt.AlignCenter)
        statusLabel.setStyleSheet("font: 30pt Arial;")
        resLabel = QLabel("\n \n \n")

        MainLayout.addLayout(searchLine)
        MainLayout.addLayout(filter)
        MainLayout.addWidget(statusLabel)
        MainLayout.addWidget(resLabel)

        self.time_to_sleep = 0 # does not allow to make orders often

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        def runEngine():


            statusLabel.setText("")
            resLabel.setText("")
            if time() - self.time_to_sleep < 5:
                statusLabel.setText("To many requests")
                return

            ordtype = self.ordertype.currentText()
            amt = amount.text()
            prc = self.price.text()
            prd = self.sLine.text()

            if len(amt) == 0 or len(prc) == 0 or len(prd) == 0:
                statusLabel.setText("Fill all \nedit lines!")
                return
            if data.orderType == "Buy" and float(amt)*float(prc) > data.balance[0]:
                statusLabel.setText("Not enough money")
                return

            req = [data.username, data.userid, ordtype, data.orderType.lower(), prd, amt, prc ]
            print("###")
            print(req)
            print("###")
            try:
                if data.goLocal:
                    raise  Exception
                print(data.username, data.password)
                res = client.process(req[1:], data.username, data.password)
            except:
                print("EXCEPTION OCCURRED: Local")
            print(res)
            print("DONE")

            if type(res) == bool or type(res[0]) == bool:
                statusLabel.setText("Not enough assets")

            elif type(res[0])!=str:
                resLabel.setText(func.resOut(res[0]))
                statusLabel.setText("Success")
                t= data.orderType[0].upper()+data.orderType[1:]
                func.Order(t,ordtype, prd, amt, prc)
                func.addToHis(t, ordtype, prd, amt, prc)
                data.addToHis = (True, [t, ordtype, prd, amt, prc])
                data.profit = res[0][-1]
                if t == "Buy":
                    data.profit = (-1)*data.profit
                data.balance = (data.balance[0]+data.profit, data.balance[1])

            elif ordtype == "Limit":
                print("fff")
                statusLabel.setText("The order stays\n in the system")
                t = data.orderType[0].upper() + data.orderType[1:] #Buy/Sell
                tt = f"\n id: { res[0] };"
                msg = func.Order(t,ordtype, prd, amt, prc +tt)
                data.addToOrd = (True,t,msg)
                req.append(res[0])
                #print(req[5], req[6])
                req[5], req[6] = float(req[5]), float(req[6])
                req[5], req[6] = str(req[5]), str(req[6])
                data.system_ord.append(req[2:])
            else:
                statusLabel.setText("Fail")
            self.time_to_sleep = time()



    def prdChanged(self):
        try:
            if self.ordertype.currentText() == "Limit":
                self.price.setText(str(data.acPrice)[0:5])
            else:
                self.price.setText(str(data.acPriceFOK)[0:5])
        except:
            pass

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", data.orderType))



