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
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor,
            )

        except Exception as ex:
            print("Соединение прервано")
            print(ex)
        self.m_app = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.m_app)
        login = self.login_EditLine.text()
        cursor = connection.cursor()
        cursor.execute(
            "select role from role_and_staff where staff in (select id from staff where login = '{}')".format(
                login
            )
        )
        role = cursor.fetchall()
        if cursor.rowcount == 1:
            for i in range(cursor.rowcount):
                print(role[i]["role"])
                if role[i]["role"] == 2:
                    print("два")
                    self.ui.tabWindet.removeTab(2)
                    self.ui.tabWindet.removeTab(2)
                if role[i]["role"] == 3:
                    print("три")
                    self.ui.tabWindet.removeTab(0)
                    self.ui.tabWindet.removeTab(0)
                    self.ui.tabWindet.removeTab(1)
                    self.ui.countStaffForBuh()
                    self.ui.salary_dep_list.clicked.connect(
                        self.ui.fin_salary_dep_widget
                    )
                if role[i]["role"] == 4:
                    print("четыре")
                    self.ui.comboBox_dep.clear()
                    cursor.execute(
                        "SELECT name_dep from department where id_dep in (select department from position where id in (select position from staff where login = '{}'))".format(
                            login
                        )
                    )
                    dep_name = cursor.fetchall()
                    self.ui.comboBox_dep.addItem(str(dep_name[0]["name_dep"]))
                    self.ui.tabWindet.removeTab(0)
                    self.ui.tabWindet.removeTab(0)
                    self.ui.tabWindet.removeTab(0)
        if cursor.rowcount == 2:
            if role[0]["role"] == 2 and role[1]["role"] == 3:
                print("два")
                self.ui.tabWindet.removeTab(3)
                self.ui.countStaffForBuh()
                self.ui.salary_dep_list.clicked.connect(self.ui.fin_salary_dep_widget)
            if role[0]["role"] == 3 and role[1]["role"] == 2:
                print("два")
                self.ui.tabWindet.removeTab(3)
                self.ui.countStaffForBuh()
                self.ui.salary_dep_list.clicked.connect(self.ui.fin_salary_dep_widget)
            if role[0]["role"] == 2 and role[1]["role"] == 4:
                print("три")
                self.ui.tabWindet.removeTab(2)
            if role[0]["role"] == 4 and role[1]["role"] == 2:
                print("три")
                self.ui.tabWindet.removeTab(2)
            if role[0]["role"] == 3 and role[1]["role"] == 4:
                print("четыре")
                self.ui.comboBox_dep.clear()
                cursor.execute(
                    "SELECT name_dep from department where id_dep in (select department from position where id in (select position from staff where login = '{}'))".format(
                        login
                    )
                )
                dep_name = cursor.fetchall()
                self.ui.comboBox_dep.addItem(str(dep_name[0]["name_dep"]))
                self.ui.tabWindet.removeTab(0)
                self.ui.tabWindet.removeTab(0)
                self.ui.countStaffForBuh()
                self.ui.salary_dep_list.clicked.connect(self.ui.fin_salary_dep_widget)
            if role[0]["role"] == 4 and role[1]["role"] == 3:
                print("четыре")
                self.ui.comboBox_dep.clear()
                cursor.execute(
                    "SELECT name_dep from department where id_dep in (select department from position where id in (select position from staff where login = '{}'))".format(
                        login
                    )
                )
                dep_name = cursor.fetchall()
                self.ui.comboBox_dep.addItem(str(dep_name[0]["name_dep"]))
                self.ui.tabWindet.removeTab(0)
                self.ui.tabWindet.removeTab(0)
                self.ui.countStaffForBuh()
                self.ui.salary_dep_list.clicked.connect(self.ui.fin_salary_dep_widget)
        self.m_app.show()

    def checkLoginPas(self):
        try:
            connection = pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor,
            )

        except Exception as ex:
            print("Соединение прервано")
            print(ex)
        cursor = connection.cursor()
        login = self.login_EditLine.text()
        pas = self.pas_EditLine.text()
        if login == "" and pas == "":
            self.label_5.setVisible(True)
        else:
            cursor.execute("select login from staff where login = '{}'".format(login))
            if cursor.rowcount == 0:
                self.label_6.setVisible(True)
                self.pas_EditLine.clear()
                self.login_EditLine.clear()
            else:
                cursor.execute(
                    "select password from staff where login = '{}'".format(login)
                )
                log = cursor.fetchall()
                if log[0]["password"] == pas:
                    self.open_main_programm()
                else:
                    self.label_5.setVisible(True)
                    self.pas_EditLine.clear()
        self.startHidden()

    def startHidden(self):
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.pas_EditLine.clear()
        self.login_EditLine.clear()

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
        self.label_5 = QtWidgets.QLabel(parent=Form)
        self.label_5.setGeometry(QtCore.QRect(320, 250, 250, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=Form)
        self.label_6.setGeometry(QtCore.QRect(320, 190, 250, 20))
        self.label_6.setObjectName("label_6")
        self.log_in_button.clicked.connect(self.checkLoginPas)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Эффективный контракт"))
        self.label.setText(_translate("Form", "Для доступа в систему"))
        self.label_2.setText(_translate("Form", "введите свой логин и пароль"))
        self.label_3.setText(_translate("Form", "Логин"))
        self.label_4.setText(_translate("Form", "Пароль"))
        self.label_5.setText(_translate("Form", "Неправильный логин и/или пароль"))
        self.label_6.setText(_translate("Form", "Такого логина не существует"))
        self.log_in_button.setText(_translate("Form", "Войти"))
        self.startHidden()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Log()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
