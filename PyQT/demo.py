import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit,\
    QVBoxLayout

from PyQt5.QtGui import QIcon


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(400, 400)

        self.setWindowTitle('Diagnosis')

        layout = QVBoxLayout()

        btn1 = QPushButton('Connecte')
        layout.addWidget(btn1)

        btn2 = QPushButton('Disconnect')
        layout.addWidget(btn2)

        btn3 = QPushButton('Close')
        layout.addWidget(btn3)

        #添加一个伸缩器（弹簧）
        layout.addStretch(2)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MyWindow()
    w.show()

    app.exec()
