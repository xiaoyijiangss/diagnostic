from QLed import QLed
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from tkinter import filedialog
from qt_material import apply_stylesheet, list_themes
import sys
# 加载UI，并可以切换qt_material风格用于快速预览的脚本。 
# 注意：ui界面文件是个对话框，那么MyApp就必须继承 QDialog
# 类似的，若ui界面文件是个MainWindow，那么MyApp就必须继承 QMainWindow

ui_file = filedialog.askopenfilename(initialdir='D://software_development_workplace//',\
                                     filetypes=[('UI files', '*.ui')])

themes = list_themes()

class MyApp(QMainWindow, QtWidgets.QDialog):
    '''to show the UI file'''
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(ui_file, self)
        self.ui.show()

class Theme_Dialog(QtWidgets.QDialog):
    '''Dialog widget to integrate the themes'''
    def __init__(self) -> None:
        super(Theme_Dialog, self).__init__()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 700)
        _gridLayout = QtWidgets.QGridLayout(Dialog)
        _gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setMinimumSize(QtCore.QSize(250, 600))
        self.listWidget.setMaximumSize(QtCore.QSize(250, 16777215))
        self.listWidget.setObjectName("listWidget")
        _gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)

        self.listWidget.addItems(list_themes())
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.listWidget.itemClicked.connect(self.sel_theme)

        
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog")) 

    def sel_theme(self, cindex):
        '''pass the selected item'text in the listwidget to apply_stlyesheet'''
        apply_stylesheet(app=myapp, theme=self.listWidget.\
                         item(self.listWidget.row(cindex)).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp() #initiate the main window
    my_the_inte = Theme_Dialog()    #initiate the UI for dialog window
    my_dia = QtWidgets.QDialog()    #initiate a dia class
    my_the_inte.setupUi(my_dia)    #set the UI to the instance

    myapp.show()
    my_dia.show()


    sys.exit(app.exec_())