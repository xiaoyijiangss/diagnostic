# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from Diagnostic_DownLoad import *
from PyDoIP import *

#pyuic5 -o Diagnostic_DownLoad.py Diagnostic_DownLoad.ui

class MyWindow(QMainWindow, Ui_MainWindow):
#class MyWindow(QWidget, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.selectECUname='0C02'

        #event
        self.pushButton_2.clicked.connect(self.ConnectToDoIPServer_)  #连接
        self.pushButton_3.clicked.connect(self.DisconnectFromDoIPServer_) #duankai
        self.comboBox_3.currentIndexChanged.connect(self.selectecu_)  #输入
        self.pushButton_13.clicked.connect(self.sendreq_)             #发送
        #self.graphicsView.setBackgroundBrush(QColor.green())
        self.radioButton_3.clicked.connect(self.DoIPSwitchDiagnosticSession_)
        self.radioButton_2.clicked.connect(self.DoIPSA_)
        self.checkBox.stateChanged.connect(self.choose)
        self.textEdit.moveCursor(self.textEdit.textCursor().End)
        self.CheckConnection()

    def CheckConnection(self):
        if DoIPClient._isTCPConnected==True:
            self.pushButton_2.setStyleSheet('''QPushButton{background:#40FF80;}''')
        else:
            self.pushButton_2.setStyleSheet('''QPushButton{background:#FFFFC0;}''')
        cc=threading.Timer(2.0, self.CheckConnection)
        cc.start()

    def selectecu_(self):
        if self.comboBox_3.currentText() == 'EGW':
            self.selectECUname='0C02'
        elif self.comboBox_3.currentText() == 'GW':
            self.selectECUname='0C03'
        else:
            self.selectECUname = '1FFF'
        self.lineEdit_2.setText(self.selectECUname)
    def sendreq_(self):
        inputcmd = self.lineEdit.text()
        imputfilter=inputcmd.replace(' ','')
        if imputfilter[0:2] == '22':
            DoIPClient._targetECUAddr=self.selectECUname
            DoIPClient.DoIPReadDID(imputfilter[2:6])
            self.textEdit.append('Client:'+DoIPClient.inputvalue+'\n'+'Server:'+DoIPClient.responsevalue)  # add log
        elif imputfilter[0:2] == '31':
            DoIPClient.DoIPRoutineControl(subfunction=imputfilter[2:4], routine_id=imputfilter[4:8], op_data=imputfilter[8:10])

    def ConnectToDoIPServer_(self):
        DoIPClient.ConnectToDoIPServer(routingActivation=True, targetECUAddr='0C02')
    def DisconnectFromDoIPServer_(self):
        DoIPClient.DisconnectFromDoIPServer()
    def RequestRoutingActivation_(self):
        DoIPClient.RequestRoutingActivation(localECUAddr='0E02', targetECUAddr='0C02')
    def DoIPSwitchDiagnosticSession_(self):
        DoIPClient.DoIPSwitchDiagnosticSession(3)
    def DoIPSA_(self):
        DoIPClient.DoIPSecurityEntry('01')

    def choose(self):
        if self.checkBox.isChecked()==True:
            self.DoIPTesterSet()
        else:
            self.DoIPTesterCancel()
    def DoIPTesterSet(self):
        DoIPClient.DoIPTesterPresent()
        #print(time.time())
        global t
        t=threading.Timer(4.0, self.DoIPTesterSet)
        t.start()
    def DoIPTesterCancel(self):
        t.cancel()

if __name__ == '__main__':
    #new class
    DoIPClient = DoIP_Client()
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())