
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QScrollArea, QVBoxLayout,QHBoxLayout, QGroupBox, QPushButton, QFormLayout, QTabWidget, QSlider
from PyQt5.QtWidgets import QMessageBox, QShortcut
from PyQt5.QtCore import QThread, Qt, pyqtSignal
import sys
import styles
from graphs import *
from random import randrange
from PyQt5.QtGui import QPixmap
import functions as func
import orderWindow as ord
import configWindow as cfg
import confirmwin
import assets
import Error
import data
import time
import os
import signal

import client

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
                        time.sleep(self.timeToSleep)
                        self.change_value.emit(cnt)
                except:
                    print("MyThread error")
        except: pass



class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Main window"
        self.top = 55
        self.left = 7
        w = data.scale[0]
        h = data.scale[1]

        data.reso[0] = App.primaryScreen().size().width()
        data.reso[1] = App.primaryScreen().size().height()
        self.width = App.primaryScreen().size().width()/w
        self.height = App.primaryScreen().size().height()/h
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        data.graphResolution = [self.width/data.scale[2], self.height/data.scale[3]]
        self.setWindowIcon(QtGui.QIcon('icon1.ico'))
        self.formLayout0 = QFormLayout()
        self.groupBox0 = QGroupBox("Available Asks")

        self.groupBox0.setLayout(self.formLayout0)
        scroll0 = QScrollArea()
        scroll0.setWidget(self.groupBox0)
        scroll0.setWidgetResizable(True)

        self.formLayout =QFormLayout()
        self.groupBox = QGroupBox("Available Bids")

        customTheme()

        data.pref_prd = list(client.get_stars(data.username, data.password))      # TODO UNCOMMENT
        #print(client.get_stars(data.username, data.password))

        self.groupBox.setLayout(self.formLayout)
        scroll = QScrollArea()
        scroll.setWidget(self.groupBox)
        scroll.setWidgetResizable(True)

        self.formLayout3 = QFormLayout()
        self.groupBox3 = QGroupBox("Your orders")



        self.groupBox3.setLayout(self.formLayout3)
        scroll3 = QScrollArea()
        scroll3.setWidget(self.groupBox3)
        scroll3.setWidgetResizable(True)


        self.formLayout1 = QFormLayout()
        self.groupBox1 = QGroupBox("Orders' History")


        history = client.get_history(data.username, data.password)
        print("HERE WE GO AGAIN")
        for r in history:
            #print(r)
            if len(r):
                Order = QtWidgets.QPushButton()
                if r[-1] == "sell":
                    sign = func.sellOrder(r[0], r[1], r[2], r[3]) # ordertype, product, amount, price
                    Order.setStyleSheet(styles.sellbutton)
                else:
                    sign = func.buyOrder(r[0], r[1], r[2], r[3])
                    Order.setStyleSheet(styles.buybutton)
                Order.setText(sign)
                Order.setDisabled(True)
                # formLayout1.addWidget(Order)
                self.formLayout1.insertRow(0, Order)



        self.groupBox1.setLayout(self.formLayout1)
        scroll2 = QScrollArea()
        scroll2.setWidget(self.groupBox1)
        scroll2.setWidgetResizable(True)





        rightArea = QVBoxLayout()

        threeScrolls = QHBoxLayout()
        threeScrolls.addWidget(scroll)
        threeScrolls.addWidget(scroll0)
        Column = QVBoxLayout()
        Column.addWidget(scroll3)
        Column.addWidget(scroll2)
        threeScrolls.addLayout(Column)
        rightArea.addLayout(threeScrolls)

        leftArea = QVBoxLayout()

        BuySell = QHBoxLayout()
        buyButton = QtWidgets.QPushButton("BUY")
        buyButton.setStyleSheet(styles.buybuttonFus.replace("text-align: left;",""))

        BuySell.addWidget(buyButton)
        sellButton = QtWidgets.QPushButton("SELL")
        sellButton.setStyleSheet(styles.sellbuttonFus.replace("text-align: left;",""))

        BuySell.addWidget(sellButton)

        settingsButton = QtWidgets.QPushButton("configuring".upper())
        BuySell.addWidget(settingsButton)
        self.MainProduct = QComboBox()
        self.MainProduct.currentIndexChanged.connect(self.prdChanged, self.MainProduct.currentIndex())

        self.MainProduct.addItem("No filter")
        for prd in data.pref_prd:
            self.MainProduct.addItem(prd)
        BuySell.addWidget(self.MainProduct)

        buy_shortcut = QShortcut(QtGui.QKeySequence("B"), self)
        buy_shortcut.activated.connect(lambda: callOrderWindow("Buy"))

        sell_shortcut = QShortcut(QtGui.QKeySequence("S"), self)
        sell_shortcut.activated.connect(lambda: callOrderWindow("Sell"))

        conf_shortcut = QShortcut(QtGui.QKeySequence("C"), self)
        conf_shortcut.activated.connect(lambda: callConfigWindow())

        my_assets = QShortcut(QtGui.QKeySequence("A"), self)
        my_assets.activated.connect(lambda: call_my_assets())




        buyButton.clicked.connect(lambda : callOrderWindow("Buy"))
        sellButton.clicked.connect(lambda: callOrderWindow("Sell"))
        settingsButton.clicked.connect(lambda: callConfigWindow())


        shortcut1 = QShortcut(QtGui.QKeySequence("1"), self)
        shortcut1.activated.connect(lambda: change_prd_keyboard(1))
        shortcut2 = QShortcut(QtGui.QKeySequence("2"), self)
        shortcut2.activated.connect(lambda: change_prd_keyboard(2))
        shortcut3 = QShortcut(QtGui.QKeySequence("3"), self)
        shortcut3.activated.connect(lambda: change_prd_keyboard(3))
        shortcut4 = QShortcut(QtGui.QKeySequence("4"), self)
        shortcut4.activated.connect(lambda: change_prd_keyboard(4))
        shortcut5 = QShortcut(QtGui.QKeySequence("5"), self)
        shortcut5.activated.connect(lambda: change_prd_keyboard(5))
        shortcut6 = QShortcut(QtGui.QKeySequence("6"), self)
        shortcut6.activated.connect(lambda: change_prd_keyboard(6))
        shortcut7 = QShortcut(QtGui.QKeySequence("7"), self)
        shortcut7.activated.connect(lambda: change_prd_keyboard(7))
        shortcut8 = QShortcut(QtGui.QKeySequence("8"), self)
        shortcut8.activated.connect(lambda: change_prd_keyboard(8))
        shortcut9 = QShortcut(QtGui.QKeySequence("9"), self)
        shortcut9.activated.connect(lambda: change_prd_keyboard(9))
        shortcut0 = QShortcut(QtGui.QKeySequence("0"), self)
        shortcut0.activated.connect(lambda: change_prd_keyboard(0))

        shortcutR = QShortcut(QtGui.QKeySequence("F5"), self)
        shortcutR.activated.connect(lambda: self.F5_EVENT())


        leftArea.addLayout(BuySell)

        graphsArea = QVBoxLayout()

        self.graph1 = CanvasUp()

        self.graph2 = CanvasLow()


        self.sliderUP = QSlider(Qt.Horizontal)

        self.sliderUP.setTickInterval(10)
        self.sliderUP.setSingleStep(30)

        self.sliderUP.valueChanged.connect(lambda: self.sliderChanged1())

        self.sliderDOWN = QSlider(Qt.Horizontal)

        self.sliderDOWN.setTickInterval(10)
        self.sliderDOWN.setSingleStep(30)
        self.sliderDOWN.valueChanged.connect(lambda: self.sliderChanged2())

        self.load = QtWidgets.QLabel()
        self.load1 = QtWidgets.QLabel()

        self.tabs = QTabWidget()
        self.graphUP = QWidget()
        self.graphUP.layout = QVBoxLayout( self.graphUP)
        self.graphUP.layout.addWidget(self.graph1)
        self.graphUP.layout.addWidget(self.sliderUP)
        self.tabs.setFixedHeight(data.graphResolution[0])
        self.tabs.setFixedWidth(data.graphResolution[1])
        self.tabs.addTab(self.graphUP, "Graph1")


        graphsArea.addWidget(self.tabs)

        self.tabs1 = QTabWidget()
        self.graphLOW = QWidget()
        self.graphLOW.layout = QVBoxLayout(self.graphLOW)
        self.graphLOW.layout.addWidget(self.graph2)
        self.graphLOW.layout.addWidget(self.sliderDOWN)
        self.tabs1.setFixedHeight(data.graphResolution[0])
        self.tabs1.setFixedWidth(data.graphResolution[1])

        self.tabs1.addTab(self.graphLOW, "Graph2")

        graphsArea.addWidget(self.tabs1)


        leftArea.addLayout(graphsArea)

        global bar
        bar = QPushButton(func.barInfo())
        bar.setStyleSheet(styles.barstyle1)
        bar.clicked.connect(lambda: call_my_assets())


        lowBar = QPushButton("NEWS:  "+ data.news[randrange(0, len(data.news))])
        lowBar.setStyleSheet(styles.news)
        lowBar.setDisabled(True)



        Mainlayout = QVBoxLayout(self)
        ContentArea = QHBoxLayout()
        ContentArea.addLayout(leftArea)
        ContentArea.addLayout(rightArea)
        Mainlayout.addWidget(bar)
        Mainlayout.addLayout(ContentArea)
        Mainlayout.addWidget(lowBar)


        self.show()

        self.thread = MyThread()  #time
        self.thread.timeToSleep = 0.3
        self.thread.change_value.connect(lambda : setProgressVal())
        self.thread.start()

        self.thread1 = MyThread() # add possible orders
        self.thread1.timeToSleep = 2.5
        self.thread1.change_value.connect(lambda: self.getUpdate())
        self.thread1.start()

        self.thread2 = MyThread() # update graphs
        self.thread2.timeToSleep = 4
        self.thread2.change_value.connect(lambda: self.updateGraphs())
        self.thread2.start()

        self.thread3 = MyThread()  # update news
        self.thread3.timeToSleep = 7
        self.thread3.change_value.connect(lambda: printNews())
        self.thread3.start()





        def setProgressVal():
            bar.setText(func.barInfo())

        def change_prd_keyboard(i):
            try:
                if i == 0:
                    self.MainProduct.setCurrentIndex(0)
                elif len(data.pref_prd) > i-1:
                    self.MainProduct.setCurrentIndex(i)
                else:
                    self.MainProduct.setCurrentIndex(0)
            except: print("error in change_prd_keyboard")


        def callConfigWindow():

            data.orderResolution[0], data.orderResolution[1] = self.width / 2.3, self.height / 1.7
            Dialog = QtWidgets.QDialog()
            ui = cfg.Ui_DialogConfig()
            ui.setupUi(Dialog)
            Dialog.exec_()
            if data.mode == "Dark":
                switchDark()
                bar.setStyleSheet(styles.barstyle2)
            else:
                QtWidgets.QApplication.instance().setPalette(self.style().standardPalette())
                switchLight()
                bar.setStyleSheet(styles.barstyle1)
            if data.clearHis == True:
                try:
                    for i in reversed(range(self.formLayout1.count())):
                        self.formLayout1.itemAt(i).widget().deleteLater()
                except:
                    pass
            data.clearHis = False


            if data.addToBox[0]:
                self.MainProduct.clear()
                self.MainProduct.addItem("No filter")
                for prd in data.pref_prd:
                    self.MainProduct.addItem(prd)
            data.addToBox = [False, []]

            if data.joinG[0] == True and data.joinG[1] == True:
                self.updateGraphs()


            self.graph1.upd()
            self.graph2.upd()


            if self.MainProduct.currentText() == "No filter":
                self.graph1.clear()
                self.graph1.no_data()
                self.graph2.clear()
                self.graph2.no_data()


            if data.joinG[0] == True and data.joinG[1] == True:
                data.zoom1 = data.zoom
                tm = time.time()
                step = 3600
                tm_ = tm - 60 * 60 * 24
                inp = [[x, x + step] for x in range(int(tm_), int(tm), int(step))]
                prd = self.MainProduct.currentText()
                data.bx = client.box_graph(prd, inp)
                #data.bx1 = client.box_graph(prd, inp)
                data.bx_lab = inp
                #print("Box", inp)

            data.box_reload = 0


        def call_my_assets():
            data.orderResolution[0], data.orderResolution[1] = self.width / data.scale_[0], self.height / data.scale_[1]
            Dialog = QtWidgets.QDialog()
            ui = assets.Ui_DialogAssets()
            ui.setupUi(Dialog)
            Dialog.exec_()




        def callOrderWindow(type):
            data.orderWinIsON = True
            data.orderResolution[0], data.orderResolution[1] = self.width /  data.scale_[2], self.height /  data.scale_[3]
            data.orderType = str(type)
            if self.MainProduct.currentText() != "No filter":
                try:
                    amtN = 0 # для средневзвешенного
                    wcc = 0
                    # computing autocomplete prices
                    if str(type) == "Buy":


                        for i in reversed(range(self.formLayout0.count())):
                            try:
                                #print("=>",func.getPrice(self.formLayout0.itemAt(i).widget().text()))
                                amtN += float(func.getAmt(self.formLayout0.itemAt(i).widget().text()))

                                wcc += float(func.getAmt(self.formLayout0.itemAt(i).widget().text()))*float(func.getPrice(self.formLayout0.itemAt(i).widget().text()))
                            except:
                                pass

                        data.acPrice = func.getPrice(self.formLayout0.itemAt(0).widget().text())
                        #print("wcc1",wcc, amtN)
                        data.acPriceFOK = (wcc/(amtN))

                    else:
                        for i in reversed(range(self.formLayout.count())):
                            try:
                                amtN += float(func.getAmt(self.formLayout.itemAt(i).widget().text()))
                                wcc += float(func.getAmt(self.formLayout.itemAt(i).widget().text()))*float(func.getPrice(self.formLayout.itemAt(i).widget().text()))
                            except:
                                pass
                        #print("wcc2", wcc, amtN)
                        data.acPrice = func.getPrice(self.formLayout.itemAt(self.formLayout.count() - 1).widget().text())
                        data.acPriceFOK = wcc/(amtN)
                except: pass

            data.autocomplete = self.MainProduct.currentText()
            Dialog = QtWidgets.QDialog()
            ui = ord.Ui_DialogOrder()
            ui.setupUi(Dialog)
            Dialog.exec_()

            if data.addToHis[0]: ### ALSO CHECKS FOR SUCCESS
                sign = func.Order(data.addToHis[1][0], data.addToHis[1][1],
                                  data.addToHis[1][2], data.addToHis[1][3], data.addToHis[1][4])
                newOrder = QtWidgets.QPushButton()
                newOrder.setStyleSheet(styles.buybutton)
                if data.addToHis[1][0].lower() == "sell":
                    newOrder.setStyleSheet(styles.sellbutton)
                newOrder.setDisabled(True)
                newOrder.setText(sign)
                self.formLayout1.insertRow(0, newOrder)

                bar.setText(func.barInfo())#CHEANGE BALANCE
                #RELOADING AVALIABLE ORDERS

                self.reloadData()

            elif data.addToOrd[0]:
                self.reloadData()

            if len(data.system_ord) != 0:
                self.reloadSystemOrders("")

            data.addToHis = (False, [])
            data.addToOrd = (False, "Buy", "")
            data.acPrice = ""
            bal = client.get_balance(data.username)
            data.balance = (bal, "$")
            func.putPersonalData()
            bar.setText(func.barInfo())
            data.orderWinIsON = False





        def printNews():
            i = randrange(0, len(data.news))
            lowBar.setText("NEWS:  "+ data.news[i])



    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_B:
            print("b pressed")



    def sliderChanged1(self):
        if self.MainProduct.currentText() != "No filter":
            data.zoom = self.sliderUP.value()
            self.graph1.clear()
            self.graph1.reloading()
            self.reloading()
            if len(data.graphsData) == 0:
                self.graph1.clear()
                self.graph1.no_data()




    def sliderChanged2(self):
        if self.MainProduct.currentText() != "No filter":
            data.zoom1 = self.sliderDOWN.value()
            self.graph2.clear()
            self.graph2.reloading()
            self.reloading()
            if len(data.graphsData_1) == 0:
                self.graph2.clear()
                self.graph2.no_data()

    def F5_EVENT(self):
        data.box_reload = 0
        self.reloading()
        self.updateGraphs()


    def reloading(self):
        print("__reloading__")
        try:
            if data.joinG[0] == True and data.joinG[1] == True:
                data.zoom1 = data.zoom
                tm = time.time()
                step = 3600
                tm_ = tm - 60 * 60 * 24
                inp = [[x, x + step] for x in range(int(tm_), int(tm), int(step))]
                prd = self.MainProduct.currentText()
                data.bx = client.box_graph(prd, inp)
                # data.bx1 = client.box_graph(prd, inp)
                data.bx_lab = inp
                # print("Box", inp)
            data.sleep += 1
            if data.sleep == 60:
                data.sleep = 0
            if data.zoom != 0:
                data.graphsData = client.stats(self.MainProduct.currentText(),
                                               time.time() - (1100 - data.zoom * 10), time.time() +15, "buy")

            else:
                data.graphsData = client.stats(self.MainProduct.currentText(),
                                               0, time.time()+15, "buy")
            if data.zoom1 != 0:
                data.graphsData_1 = client.stats(self.MainProduct.currentText(),
                                             time.time() - (1100 - data.zoom1 * 10), time.time() +15, "sell")

            else:
                data.graphsData_1 = client.stats(self.MainProduct.currentText(),
                                                 0, time.time()+15, "sell")
        except:
            print("Error in reloading")




    def updateGraphs(self):
        print("TIME: ",time.time() - data.working_time)
        try:
            if self.MainProduct.currentText() != "No filter":

                self.graph1.clear()
                if data.joinG[0] == True and data.joinG[1] == True:
                    self.sliderUP.setHidden(True)
                    self.graph1.plot_joint()
                else:
                    self.sliderUP.setHidden(False)
                    self.reloading()
                    self.graph1.plot()


                if data.joinG[0] == True and data.joinG[1] == True:

                    if data.box_reload < 1:
                        self.sliderDOWN.setHidden(True)
                        self.graph2.clear()
                        self.graph2.candels()
                        data.box_reload +=1
                else:
                    self.graph2.clear()
                    self.graph2.plot()
                    self.sliderDOWN.setHidden(False)


            else:
                data.graphsData = []
                data.graphsData_1 = []
        except: print("Error in update graphs")



    def prdChanged(self):
        data.chosen_prd = self.MainProduct.currentText()
        data.box_reload = 0
        self.sliderChanged1()
        self.sliderChanged2()
        if self.MainProduct.currentText() == "No filter":
            if not data.FIRSTSTART:
                self.graph1.clear()
                self.graph1.no_data()
                self.graph2.clear()
                self.graph2.no_data()
            data.FIRSTSTART = False

        self.reloadData()


    def reloadData(self):
        if data.joinG[0] == True and data.joinG[1] == True:
            data.sleep = 0

        try:
            text = self.MainProduct.currentText()
            data.prd = text
            res1 =[]
            res2 = []
            if text == "No filter":
                try:
                    if data.goLocal:
                        raise  Exception

                except:
                    print("EXCEPTION OCCURRED: Local database is used instead ")


            else:
                try:
                    if data.goLocal:
                        raise  Exception
                    res1 = client.exe("SELECT * FROM orders WHERE product='{}' AND request='{}'ORDER BY price LIMIT 20".format(text,
                                                                                                                   "sell"))
                    res2 = client.exe("SELECT * FROM orders WHERE product='{}' AND request='{}'ORDER BY price LIMIT 20".format(text,
                                                                                                                     "buy"))
                except:
                    print("EXCEPTION OCCURRED: Local database is used instead ")
                    res = func.findOrder(text)

            res = client.exe(f"SELECT * FROM orders WHERE uid={float(data.userid)}")

            data.yourOrd = data.system_ord

            data.system_ord = []




            try:
                for i in reversed(range(self.formLayout.count())):
                    self.formLayout.itemAt(i).widget().deleteLater()
            except:
                pass
            j2 = 0
            for order in res:
                j2+=1
                if order[3] == "sell":
                    if order[-1] == float(data.userid):
                        sys_ord = [order[2], order[3], order[4], str(order[5]), str(order[6]), str(order[0])]
                        if sys_ord not in data.system_ord:
                            data.system_ord.append(sys_ord)
                            data.ORDDIC[order[0]] = order
                    else:
                        if order not in data.Orders:
                            data.ORDDIC[order[0]] = order



            try:
                for i in reversed(range(self.formLayout0.count())):
                    self.formLayout0.itemAt(i).widget().deleteLater()
            except:
                pass
            j3 = 0
            for order in res:
                j3 +=1
                if order[3] == "buy":
                    if order[-1] == float(data.userid):
                        sys_ord = [order[2], order[3], order[4], str(order[5]), str(order[6]), str(order[0])]
                        if sys_ord not in data.system_ord:

                            data.system_ord.append(sys_ord)
                            data.ORDDIC[order[0]] = order
                    else:
                       if order not in data.Orders:
                           data.ORDDIC[order[0]]=order

                    # add to history
            try:
                for el in data.yourOrd:

                    if el not in data.system_ord and not data.orderWinIsON:
                        msg = QMessageBox()
                        msg.setWindowTitle("An order's been executed")
                        msg.setIconPixmap(QPixmap("arrow.png").scaled(80, 80))
                        msg_text = "This order\n"

                        thisorder = QPushButton()
                        if el[1] == "buy":
                            thisorder.setStyleSheet(styles.buybutton)
                            thisorder.setText(func.buyOrder("Limit", el[2], el[3], el[4]))
                            data.balance = (data.balance[0]- float(el[3]) * float(el[4]), data.balance[1])
                            #msg_text += func.buyOrder("Limit", el[2], el[3], el[4])
                            msg_text += "Limit Buy" + el[2]
                        else:
                            thisorder.setStyleSheet(styles.sellbutton)
                            thisorder.setText(func.sellOrder("Limit", el[2], el[3], el[4]))
                            data.balance = (data.balance[0] + float(el[3]) * float(el[4]), data.balance[1])
                            #msg_text += func.sellOrder("Limit", el[2], el[3], el[4])
                            msg_text += "Limit Sell" + el[2]
                        thisorder.setDisabled(True)
                        self.formLayout1.insertRow(0, thisorder)
                        msg.setText(msg_text + "\nhas been executed.")
                        msg.setWindowIcon(QtGui.QIcon('bgicon.ico'))
                        msg.exec_()
            except:
                print("line 676")




            res = res1 + res2
            if self.MainProduct.currentText() != "No filter":
                prices = func.merger(res)
                for el in prices:
                        if prices[el][1][3] == "sell":
                            thisorder = QPushButton()
                            thisorder.setStyleSheet(styles.sellbutton)
                            sign = func.sellOrder(prices[el][1][2], prices[el][1][4], str(prices[el][0]), prices[el][1][6])
                            thisorder.setText(sign)
                            self.formLayout0.addRow(thisorder)
                        else:
                            thisorder = QPushButton()
                            thisorder.setStyleSheet(styles.buybutton)
                            sign = func.buyOrder(prices[el][1][2], prices[el][1][4], str(prices[el][0]), prices[el][1][6])
                            thisorder.setText(sign)
                            self.formLayout.insertRow(0,thisorder)

            self.reloadSystemOrders("")


        except:
            print("Error in def reloadData")
            if data.error == False:
                data.error = True
                connect()

    def removeOrder(self, n):

        oldstyle =  self.formLayout3.itemAt(n-1).widget().styleSheet()
        self.formLayout3.itemAt(n-1).widget().setStyleSheet(styles.buttonY)
        data.orderResolution[0], data.orderResolution[1] = self.width / 2.5, self.height / 1.3
        Dialog = QtWidgets.QDialog()
        ui = confirmwin.Ui_DialogCONFIRM()
        ui.setupUi(Dialog)
        Dialog.exec_()
        try:
            if data.toDelete:
                client.delete(data.username, data.system_ord[n - 1][-1])
                for i in reversed(range(self.formLayout3.count())):
                    self.formLayout3.itemAt(i).widget().deleteLater()
                del data.system_ord[n - 1]
                self.reloadSystemOrders("")
                bal = client.get_balance(data.username)
                data.balance = (bal, "$")
                func.putPersonalData()
                bar.setText(func.barInfo())
            else:
                self.formLayout3.itemAt(n - 1).widget().setStyleSheet(oldstyle)
            data.toDelete = False
        except:
            print("Error in remove order")


    def reloadSystemOrders(self, temp):
        try:
            for i in reversed(range(self.formLayout3.count())):
                self.formLayout3.itemAt(i).widget().deleteLater()
            j1 = 0
            for el in data.system_ord:
                j1 += 1
                thisorder = QPushButton("",
                                        clicked=lambda _, n=j1: self.removeOrder(n))
                if el[1] == "buy":

                    thisorder.setStyleSheet(styles.buybutton)
                    thisorder.setText(func.buyOrder("Limit", el[2], el[3], el[4] +"\n id: " +el[-1]))
                else:

                    thisorder.setStyleSheet(styles.sellbutton)
                    thisorder.setText(func.sellOrder("Limit", el[2], el[3], el[4] + "\n id: " + el[-1]))
                self.formLayout3.insertRow(0, thisorder)
        except: print("Error reloadSystemOrders")


    def getUpdate(self):
        self.reloadData()

    def closeEvent(self, event):

        print("Goodbye")
        # TODO приложение работает в фоновом режиме даже после закрытия
        self.thread.terminate()
        self.thread1.terminate()
        self.thread2.terminate()
        self.thread3.terminate()

        pid = os.getpid()
        os.kill(pid, signal.SIGINT)
        print(pid)
        print("BYE")








def connect():

    Dialog = QtWidgets.QDialog()
    ui = Error.Error()
    ui.setupUi(Dialog)
    Dialog.exec_()

def customTheme():
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(0, 0, 0).lighter())
    #App.setPalette(palette) # TODO SET PALLETE


def switchDark():

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, Qt.white)
    palette.setColor(QtGui.QPalette.Text, Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, Qt.red)
    palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    palette.setColor(QtGui.QPalette.HighlightedText, Qt.black)

    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    App.setPalette(palette)

def switchLight():
    palette = QtGui.QPalette()
    # do stuff
    App.setPalette(palette)

def runGUI():
    global App, window
    App = QApplication(sys.argv)
    App.setStyle('Fusion')
    window = MainWindow()
    sys.exit(App.exec())


if __name__ == '__main__':
    try:
        data.working_time = time.time()
        runGUI()
        App = QApplication(sys.argv)
        App.setStyle('Fusion')
        window = MainWindow()
        print("APP CLOSES")
        sys.exit(App.exec())

    except Exception as F:
        print(F)

