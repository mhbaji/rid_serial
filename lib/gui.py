from PyQt5 import QtCore, QtGui, QtWidgets
from lib.lib_serial import Lib_Serial
from datetime import date, datetime

class Ui_RidSerial(object):
    ports = []
    isStop = True
    isConnected = False
    def setupUi(self, RidSerial):
        RidSerial.setObjectName("RidSerial")
        RidSerial.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(RidSerial)
        self.centralwidget.setObjectName("centralwidget")
        self.cb_port = QtWidgets.QComboBox(self.centralwidget)
        self.cb_port.setGeometry(QtCore.QRect(100, 20, 150, 25))
        self.cb_port.setObjectName("cb_port")
        self.cb_baudrate = QtWidgets.QComboBox(self.centralwidget)
        self.cb_baudrate.setGeometry(QtCore.QRect(400, 20, 150, 25))
        self.cb_baudrate.setObjectName("cb_baudrate")
        self.lbl_port = QtWidgets.QLabel(self.centralwidget)
        self.lbl_port.setGeometry(QtCore.QRect(20, 20, 71, 17))
        self.lbl_port.setObjectName("lbl_port")
        self.lbl_baudrate = QtWidgets.QLabel(self.centralwidget)
        self.lbl_baudrate.setGeometry(QtCore.QRect(300, 20, 71, 17))
        self.lbl_baudrate.setObjectName("lbl_baudrate")
        self.pb_start_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pb_start_stop.setGeometry(QtCore.QRect(620, 20, 89, 25))
        self.pb_start_stop.setObjectName("pb_start_stop")
        self.tb_result = QtWidgets.QTextBrowser(self.centralwidget)
        self.tb_result.setGeometry(QtCore.QRect(20, 80, 751, 661))
        self.tb_result.setObjectName("tb_result")
        RidSerial.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RidSerial)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        RidSerial.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RidSerial)
        self.statusbar.setObjectName("statusbar")
        RidSerial.setStatusBar(self.statusbar)

        self.init_system()

        self.retranslateUi(RidSerial)
        QtCore.QMetaObject.connectSlotsByName(RidSerial)

    def retranslateUi(self, RidSerial):
        _translate = QtCore.QCoreApplication.translate
        RidSerial.setWindowTitle(_translate("RidSerial", "RID Serial"))
        self.lbl_port.setText(_translate("RidSerial", "Port"))
        self.lbl_baudrate.setText(_translate("RidSerial", "Baudrate"))
        self.pb_start_stop.setText(_translate("RidSerial", "Start"))

    def init_system(self):
        self.find_ports()
        self._view_list_baudrate()
        self.init_serial()
        self.pb_start_stop.clicked.connect(self.action_start_stop)
    
    def action_start_stop(self):
        if self.isStop:
            self._action_start()
        else:
            self._action_stop()
    
    def _action_start(self):
        port = self.cb_port.currentText()
        if len(port) > 0:
            _baudrate = self.cb_baudrate.currentText()
            _int_baudrate = int(_baudrate)
            self.serial.set(port, _int_baudrate)
            
            try:
                self.serial.connect()
                self.isConnected = True
            except Exception as ex:
                print('ex', ex)
                self.isConnected = False

            if self.isConnected:
                self.serial.start()
                self.pb_start_stop.setText("Stop")
                self.isStop = False

    def _action_stop(self):
        self.serial.stop()
        self.pb_start_stop.setText("Start")
        self.isStop = True

    def init_serial(self):
        self.serial = Lib_Serial()
        self.serial.signal_serial.connect(self._update_serial)
    
    def _update_serial(self, str_value):
        now = datetime.now()
        str_split = str_value.split(',')
        _digit = []
        for splt in str_split:
            _tmp = ''
            for x in splt:
                if x.isdigit() or x == '.':
                    _tmp+=x

            try:
                _tmp_digit = int(_tmp)
            except:
                _tmp_digit = float(_tmp)
                pass

            _digit.append(_tmp_digit)
        
        _format_append = "{} {}".format(str_split, _digit)
        self._append_result(now, _format_append)
    
    def _append_result(self, now, msg):
        self.tb_result.append("[{}] {}".format(self._get_time(now), msg))

    def _get_time(self, now):
        _format_time = "{}:{}:{}".format(now.hour, now.minute, now.second)
        return _format_time

    def find_ports(self):
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()

        self.ports = []
        for port, desc, hwid in sorted(ports):
            self.ports.append(port)
            self.cb_port.addItem(port)

    def _view_list_baudrate(self):
        list_baudrate = [9600, 57600, 115200]
        for _baudrate in list_baudrate:
            self.cb_baudrate.addItem(str(_baudrate))
            