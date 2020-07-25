from entrance import *
from PyQt5 import QtWidgets
import warnings


def startApp():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    startApp()


