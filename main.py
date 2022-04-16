import sys
from PyQt5 import QtWidgets
from lib.guiV1 import Ui_RidSerial

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui_dws = Ui_RidSerial()
    ui_dws.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    