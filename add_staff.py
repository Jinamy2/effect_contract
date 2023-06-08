from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd


class Ui_Add_Staff(object):
    def addStaffToBD(self):
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
        fio = self.staff_lineEdit.text().split()
        fam = fio[0]
        name = fio[1]
        if len(fio) == 2:
            otch = ""
        else:
            otch = fio[2]
        pos = self.pos_comboBox.currentText()
        log = self.staff_log_lineEdit.text()
        pas = self.staff_log_lineEdit_2.text()
        dep = self.dep_line.text()
        cursor.execute(
            "INSERT INTO `staff` (`id`, `fam`, `name`, `otch`, `login`, `password`, `position`) VALUES (NULL, '{}', '{}', '{}', '{}', '{}', (select id from position where name_pos = '{}' and department in (select id_dep from department where name_dep='{}')));".format(
                fam, name, otch, log, pas, pos, dep
            )
        )
        connection.commit()
        if self.role_lineEdit.text() != "":
            roles = self.role_lineEdit.text().split(",")
            staff = self.staff_lineEdit.text()
            for i in range(len(roles)):
                cursor.execute(
                    "INSERT INTO `role_and_staff` (`id`, `role`, `staff`) VALUES (NULL, '{}', (select id from staff where CONCAT(fam, ' ', name, ' ',otch) = '{}' and position in (select id from position where position.name_pos = '{}' and position.department in (select department.id_dep from department where department.name_dep = '{}'))));".format(
                        roles[i], staff, pos, dep
                    )
                )
                connection.commit()
        connection.close()

    def setupUi(self, Add_Staff):
        Add_Staff.setObjectName("Add_Staff")
        Add_Staff.resize(482, 430)
        self.label = QtWidgets.QLabel(parent=Add_Staff)
        self.label.setGeometry(QtCore.QRect(40, 80, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.staff_lineEdit = QtWidgets.QLineEdit(parent=Add_Staff)
        self.staff_lineEdit.setGeometry(QtCore.QRect(100, 70, 361, 31))
        self.staff_lineEdit.setObjectName("staff_lineEdit")
        self.dep_line = QtWidgets.QLineEdit(parent=Add_Staff)
        self.dep_line.setGeometry(QtCore.QRect(100, 70, 1, 1))
        self.dep_line.setObjectName("dep_line")
        self.label_2 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_2.setGeometry(QtCore.QRect(30, 130, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pos_comboBox = QtWidgets.QComboBox(parent=Add_Staff)
        self.pos_comboBox.setGeometry(QtCore.QRect(140, 120, 321, 31))
        self.pos_comboBox.setObjectName("pos_comboBox")
        self.label_3 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_3.setGeometry(QtCore.QRect(30, 180, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.staff_log_lineEdit = QtWidgets.QLineEdit(parent=Add_Staff)
        self.staff_log_lineEdit.setGeometry(QtCore.QRect(100, 170, 361, 31))
        self.staff_log_lineEdit.setObjectName("staff_log_lineEdit")
        self.label_4 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.staff_log_lineEdit_2 = QtWidgets.QLineEdit(parent=Add_Staff)
        self.staff_log_lineEdit_2.setGeometry(QtCore.QRect(100, 220, 361, 31))
        self.staff_log_lineEdit_2.setObjectName("staff_log_lineEdit_2")
        self.role_lineEdit = QtWidgets.QLineEdit(parent=Add_Staff)
        self.role_lineEdit.setGeometry(QtCore.QRect(100, 275, 361, 31))
        self.role_lineEdit.setObjectName("role_lineEdit")
        self.label_5 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_5.setGeometry(QtCore.QRect(230, 196, 111, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_6.setGeometry(QtCore.QRect(230, 250, 111, 20))
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_9.setGeometry(QtCore.QRect(230, 300, 111, 20))
        self.label_9.setObjectName("label_9")
        self.label_7 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_7.setGeometry(QtCore.QRect(150, 10, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_7 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_7.setGeometry(QtCore.QRect(150, 10, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=Add_Staff)
        self.label_8.setGeometry(QtCore.QRect(30, 280, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.add_staff_in_bd = QtWidgets.QPushButton(parent=Add_Staff)
        self.add_staff_in_bd.setGeometry(QtCore.QRect(40, 350, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_staff_in_bd.setFont(font)
        self.add_staff_in_bd.setObjectName("add_staff_in_bd")
        self.hide_staff_in_bd = QtWidgets.QPushButton(parent=Add_Staff)
        self.hide_staff_in_bd.setGeometry(QtCore.QRect(300, 350, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hide_staff_in_bd.setFont(font)
        self.hide_staff_in_bd.setObjectName("hide_staff_in_bd")

        self.retranslateUi(Add_Staff)
        QtCore.QMetaObject.connectSlotsByName(Add_Staff)
        self.add_staff_in_bd.clicked.connect(self.addStaffToBD)

    def retranslateUi(self, Add_Staff):
        _translate = QtCore.QCoreApplication.translate
        Add_Staff.setWindowTitle(_translate("Add_Staff", "Создать сотрудника"))
        self.label.setText(_translate("Add_Staff", "ФИО"))
        self.label_2.setText(_translate("Add_Staff", "Должность"))
        self.label_3.setText(_translate("Add_Staff", "Логин"))
        self.label_4.setText(_translate("Add_Staff", "Пароль"))
        self.label_5.setText(_translate("Add_Staff", "(не обязательно)"))
        self.label_6.setText(_translate("Add_Staff", "(не обязательно)"))
        self.label_7.setText(_translate("Add_Staff", "Добавить сотрудника"))
        self.label_8.setText(_translate("Add_Staff", "Роль"))
        self.label_9.setText(_translate("Add_Staff", "(не обязательно)"))
        self.add_staff_in_bd.setText(_translate("Add_Staff", "Готово"))
        self.hide_staff_in_bd.setText(_translate("Add_Staff", "Отмена"))
        self.dep_line.setVisible(False)
        text = "Перечислите через запятую роли сотрудника. 2-Кадры, 3-Бухгалтер, 4-Рук.отдела, 5-Администратор"
        self.role_lineEdit.setToolTip(text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Add_Staff = QtWidgets.QWidget()
    ui = Ui_Add_Staff()
    ui.setupUi(Add_Staff)
    Add_Staff.show()
    sys.exit(app.exec())
