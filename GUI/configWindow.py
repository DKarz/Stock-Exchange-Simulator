import data
import functions as func
from PyQt5 import QtCore, QtGui, QtWidgets
from client import bug_log
import client
from PyQt5.QtWidgets import QGridLayout, QWidget, QTabWidget,QScrollArea, QVBoxLayout,QHBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout, QCheckBox

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)





class Ui_DialogConfig(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")

        Dialog.resize(data.orderResolution[0], data.orderResolution[1])
        addingToBox = []
        mainWin = QVBoxLayout(Dialog)
        tabs = QTabWidget()
        mainWin.addWidget(tabs)
        apply = QPushButton("Apply and Close")
        apply.clicked.connect(lambda : applyClose())
        mainWin.addWidget(apply)
        apply.setFixedWidth(data.orderResolution[0]/5)
        Dialog.setWindowIcon(QtGui.QIcon('gear.ico'))
        tabs.resize(data.orderResolution[0], data.orderResolution[1])
        tab1 = QWidget()
        tab1.layout = QGridLayout(tab1)
        deleteHisButton = QPushButton("DELETE HIST.")
        deleteHisButton.clicked.connect(lambda : deleteHis())
        deleteHisButton.setFixedWidth(data.orderResolution[0]/5)

        darkModeBut = QPushButton()
        if data.mode == "Light":
            darkModeBut.setText("DARK MODE")
        else:
            darkModeBut.setText("Light MODE")

        darkModeBut.clicked.connect(lambda: switchToDark())
        tab1.layout.addWidget(deleteHisButton)
        tab1.layout.addWidget(darkModeBut)
        darkModeBut.setFixedWidth(data.orderResolution[0] / 5)

        tab1.layout.addWidget(QLabel("Find bag? Say about it:"), 2, 0)
        space = QtWidgets.QTextEdit()
        tab1.layout.addWidget(space,3,0)
        sendBag = QPushButton("Send")
        sendBag.clicked.connect(lambda: send_bug())
        tab1.layout.addWidget(sendBag, 3, 1)




        tabs.addTab(tab1, "General")

        #tab2 = QWidget()
        #tab2.layout = QVBoxLayout(tab2)
        #tabs.addTab(tab2, "Graph Settings")


        # searchLine = QHBoxLayout()
        # sLine = QtWidgets.QLineEdit()
        # sBut = QPushButton("Search")
        # sBut.clicked.connect(lambda: search())
        # searchLine.addWidget(sLine)
        # searchLine.addWidget(sBut)


        joinGraphs = QCheckBox("Join Buy and Sell Graphs?")
        if data.joinG[1] == True:
            joinGraphs.setChecked(True)
        joinGraphs.stateChanged.connect(self.joinGraphs)
        tab1.layout.addWidget(joinGraphs, 0, 1)

        tab4 = QWidget()
        tab4.layout = QVBoxLayout(tab4)
        tabs.addTab(tab4, "Products")
        tab4.layout.addWidget(QLabel("Find products you want to add."))
        searchLine1 = QHBoxLayout()
        sLine1 = QtWidgets.QLineEdit()
        sBut1 = QPushButton("Add")
        sBut1.clicked.connect(lambda: addPrd())
        searchLine1.addWidget(sLine1)
        searchLine1.addWidget(sBut1)
        tab4.layout.addLayout(searchLine1)

        formLayout1 = QFormLayout()

        groupBox1 = QGroupBox()
        i = 0
        for prod in data.pref_prd:
            i +=1
            t = QPushButton("    "+prod, clicked=lambda _, n=i: remove_prd(n-1))
            t.setFixedWidth(data.orderResolution[0] / 5)
            t.setStyleSheet("text-align: left;")
            formLayout1.insertRow(0, t)


        groupBox1.setLayout(formLayout1)
        groupBox1.setTitle("Your products:     Click to delete from Your Products.")
        scroll1 = QScrollArea()
        scroll1.setWidget(groupBox1)
        scroll1.setWidgetResizable(True)

        tab4.layout.addWidget(scroll1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        def addPrd():
            prd = sLine1.text()
            data.pref_prd.append(prd)
            t = QPushButton("    "+str(prd))
            t.setFixedWidth(data.orderResolution[0] / 5)
            t.setStyleSheet("text-align: left;")
            formLayout1.addRow(t)
            addingToBox.append(prd)
            data.addToBox = [True, addingToBox]


        def send_bug():
            text = space.toPlainText()
            sendBag.setText("DONE")
            sendBag.setDisabled(True)

            bug_log(func.log_text_format(text))





        def applyClose():
            if data.joinG[0] == True:
                data.joinG = [True, True]
            if len(addingToBox) != 0:
                client.add_star(addingToBox,data.username,data.password)
            Dialog.close()

        def switchToDark():
            darkModeBut.setText("Click 'Apply and Close'")
            darkModeBut.setDisabled(True)
            if data.mode == "Light":
                data.mode = "Dark"
            else:
                data.mode = "Light"

        def deleteHis():
            data.clearHis = True
            func.clearHis()
            client.delete_history(data.username, data.password)
            deleteHisButton.setText("DONE")
            deleteHisButton.setDisabled(True)


        def remove_prd(index):
            print("DLETE THIS NIBO", data.pref_prd[index])
            client.remove_star([data.pref_prd[index]], data.username, data.password)
            del data.pref_prd[index]
            for i in reversed(range(formLayout1.count())):
                formLayout1.itemAt(i).widget().deleteLater()
            i = 0
            for prod in data.pref_prd:
                i += 1
                t = QPushButton("    "+prod, clicked=lambda _, n=i: remove_prd(n - 1))
                t.setFixedWidth(data.orderResolution[0] / 5)
                t.setStyleSheet("text-align: left;")
                formLayout1.insertRow(0, t)
            print(data.pref_prd)

            data.addToBox = [True, ""]

    def joinGraphs(self, state):
        if state == QtCore.Qt.Checked:
            #print('Checked')
            data.joinG = [True, False]
        else:
            data.joinG = [False, False]



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Config"))



