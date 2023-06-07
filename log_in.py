from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
from PyQt6 import QtCore, QtGui, QtWidgets
from main import Ui_MainWindow


class Ui_Form_Log(object):
    def open_main_programm(self):
        self.m_app = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.m_app)
        self.m_app.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(755, 411)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(280, 20, 281, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(240, 60, 371, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(100, 150, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(100, 210, 101, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.log_in_button = QtWidgets.QPushButton(parent=Form)
        self.log_in_button.setGeometry(QtCore.QRect(310, 310, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.log_in_button.setFont(font)
        self.log_in_button.setObjectName("log_in_button")
        self.login_EditLine = QtWidgets.QLineEdit(parent=Form)
        self.login_EditLine.setGeometry(QtCore.QRect(210, 160, 431, 31))
        self.login_EditLine.setObjectName("login_EditLine")
        self.pas_EditLine = QtWidgets.QLineEdit(parent=Form)
        self.pas_EditLine.setGeometry(QtCore.QRect(210, 220, 431, 31))
        self.pas_EditLine.setObjectName("pas_EditLine")
        self.log_in_button.clicked.connect(self.open_main_programm)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Для доступа в систему"))
        self.label_2.setText(_translate("Form", "введите свой логин и пароль"))
        self.label_3.setText(_translate("Form", "Логин"))
        self.label_4.setText(_translate("Form", "Пароль"))
        self.log_in_button.setText(_translate("Form", "Войти"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Log()
    ui.setupUi(Form)
    Form.show()
    ui.log_in_button.clicked.connect(Form.close)
    sys.exit(app.exec())
