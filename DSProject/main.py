from PyQt5.QtWidgets import QMainWindow
import sys, time, binascii
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets
# from qt_material import apply_stylesheet
from ui_engineering_ds import Ui_MainWindow
from fuc_DoIP import Doip_client
import data_base_Doip as DB 
#self.Led = QLed(self.frame_3, onColour=QLed.Green, offColour=QLed.Red)


#UI-----------------------------------------------------------------------------
class MainWindowMge(QMainWindow):
    '''Main GUI Window'''

    def __init__(self) -> None:
        super(MainWindowMge, self).__init__()
        #initiate the UI
        self.ThRec = RecTcp()
        self.ThRec.updated_text.connect(self.updateText)    #triggle and send message to upgrade
        self.DoipLabs = Doip_client()
        self.ui = Ui_MainWindow()   
        self.ui.setupUi(self)
        self.rec_mm = ''
        self.send_mm = ''
        self.version_code = self.VC = DB.DOIP_PV + DB.DOIP_IPV
        
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)

        self.ui.pushButton_1.clicked.connect(self.click_connect)
        self.ui.pushButton_3.clicked.connect(self.click_send)
        self.ui.pushButton_4.clicked.connect(self.click_disconnect)

    def connection_check(self):
        '''check the condition to activate buttons'''
        if MyMainWindow.DoipLabs.TCPConnected == True:
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_4.setEnabled(True)
            self.ui.Led.value = 1
            self.ThRec.start()  #start the receiving thread
            activationString = "02fd00050000000b0e80000000000000000000"
            diagnostic_message = '02fd8001000000060e801fff3e80'
            diagnostic_message_rd = '02fd8001000000070e801a0122dd0a'
            self.send_message(activationString)
            self.send_message(diagnostic_message)
            self.send_message(diagnostic_message_rd)

    def click_connect(self):
        if MyMainWindow.DoipLabs.TCPConnected == True:
            self.ui.pushButton_1.setEnabled(False)  #disable the button "connect"
            self.ui.Led.value = 1
            self.ThRec.isPulse = False  #restart the thread

        else:
            MyMainWindow.DoipLabs.ConnectToServer()   #run the connect process 
            self.ui.lineEdit_2.setText(self.DoipLabs._local_ip +" at " + \
                                    self.DoipLabs.ethernet_name)   #source addr
            self.ui.lineEdit.setText(self.DoipLabs.tar_ip)    #target addr
            self.ui.lineEdit_3.setText(self.DoipLabs.vin)     #VIN
            self.connection_check() #run the connection check process

    def click_send(self):
        content = self.ui.textEdit.toPlainText()
        send_data = binascii.unhexlify(content)
        MyMainWindow.DoipLabs._TCP_Socket.send(send_data)
        time.sleep(0.3)
        #"02fd00050000000b0e80000000000000000000"
        #'02fd8001000000070e801a0122dd0a'

    def send_message(self, message:str):
        send_data = binascii.unhexlify(message)
        MyMainWindow.DoipLabs._TCP_Socket.send(send_data)
        time.sleep(0.1)

    def click_disconnect(self):
        MyMainWindow.DoipLabs.DisconnectToServer()
        self.ui.Led.value = 0   #turn LED to red
        self.ui.pushButton_1.setEnabled(True) #enable the connect button
        self.ThRec.cancel()   #stop the receiving thread

    def updateText( self, text ):
        # here upgrade the textbrowser content from Qthread "RecTcp"
        MyMainWindow.ui.textBrowser.append(text)


class RecTcp(QThread):
    '''receive data and show in the window'''
    valueChange = pyqtSignal(int)
    updated_text = pyqtSignal(str)  ##to updata the textbrowser
    
    def __init__(self) -> None:
        super().__init__()
        self.isPulse = False
        self.version_code = self.VC = DB.DOIP_PV + DB.DOIP_IPV
    def run(self): 
        
        while True:
            if self.isPulse:
                self.valueChange.emit(0)
                continue
            
            try:
                if MyMainWindow.DoipLabs._TCP_Socket:
                    recv_data = MyMainWindow.DoipLabs._TCP_Socket.recv(1024)
            #02FD8002000000051A010E800002FD8001000000081A010E8062DD0A02
                    if recv_data.count(self.VC)==1: #just 1 Doip message
                        print('&& type of primessage is [%s], message is [%s]' % \
                              (type(recv_data), recv_data))
                        # MyMainWindow.rec_mm += recv_data
                        # MyMainWindow.ui.textBrowser.append(recv_data) # not safe way
                        recv_data = binascii.hexlify(recv_data).decode("utf-8").upper()
                        self.updated_text.emit(recv_data)  #to updata the textbrowser
                        time.sleep(0.1)

                    elif recv_data.count(self.VC) > 1: #have more than 1 Doip message
                        recv_split = recv_data.split(self.VC)
                        for splited_message in recv_split:
                            if len(splited_message) > 0:    #would be empty result after splited
                                recv_data = self.VC + splited_message   #02fd+message
                                recv_data = binascii.hexlify(recv_data).decode("utf-8").upper()
                                self.updated_text.emit(recv_data)  #to updata the textbrowser
                                time.sleep(0.1)

            except Exception as err:
                print('## Can\'t receive message cause %s' % (err) )

        

    def cancel(self):
        self.isPulse= True
            


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)

    MyMainWindow = MainWindowMge()
    MyMainWindow.show()
    
    App.exec_()