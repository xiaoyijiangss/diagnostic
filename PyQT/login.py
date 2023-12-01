import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit,\
    QVBoxLayout

from PyQt5.QtGui import QIcon
from PyQt5 import uic


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    

    def init_ui(self):
        self.ui = uic.loadUi('D:/software_development_workspace/diagnostic/PyQT/untitled.ui')
        print(self.ui.__dict__)
        # self.user_name = self.ui.lineEdit
        # self.password = self.ui.lineEdit_2
        # login_btn = self.ui.pushButton
        # forget_btn = self.ui.pushButton_2
        # text_browser = self.ui.textBrowser
    
        # login_btn.clicked.connect(self.login)

        self.ed1 = self.ui.textEdit
        self.bt1 = self.ui.pushButton
        self.displayer = self.ui.textBrowser
        self.bt1.clicked.connect(self.display1)


        

    def login(self):
        print('>> 正在登录。。。')
        print(self.user_name.text())
        print(self.password.text())

    def display1(self):
        t1 = self.ed1.toPlainText()
        self.displayer.setPlainText(t1)






app = QApplication(sys.argv)

w = MyWindow()

w.ui.show()

app.exec()