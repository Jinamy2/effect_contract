from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd


class Ui_Form(object):
    def loadDep(self):
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
        self.combo_dep.clear()
        cursor = connection.cursor()
        cursor.execute("select name_dep from department;")
        result = cursor.fetchall()
        for row_number, data in enumerate(result):
            self.combo_dep.addItem("")
            self.combo_dep.setItemText(row_number, data["name_dep"])
        connection.close()

    def loadPos(self):
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
        dep = self.combo_dep.currentText()
        self.pos_combo.clear()
        cursor = connection.cursor()
        cursor.execute(
            "select name_pos from position where department in (select id_dep from department where name_dep = '{}');".format(
                dep
            )
        )
        result = cursor.fetchall()
        for row_number, data in enumerate(result):
            self.pos_combo.addItem("")
            self.pos_combo.setItemText(row_number, data["name_pos"])
        connection.close()

    def addPosInGroup_BD(self):
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
        name_gr = self.gr_name_line.text()
        name_dep = self.combo_dep.currentText()
        name_pos = self.pos_combo.currentText()
        cursor.execute(
            "INSERT INTO `pos_and_group` (`id`, `id_group`, `id_pos`) VALUES (NULL,(select id from position_group where name_group = '{}') , (SELECT id from position where name_pos='{}' and department in (select id_dep from department where name_dep = '{}')))".format(
                name_gr, name_pos, name_dep
            )
        )
        connection.commit()
        connection.close()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(541, 218)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(180, 10, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_8 = QtWidgets.QLabel(parent=Form)
        self.label_8.setGeometry(QtCore.QRect(30, 60, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.combo_dep = QtWidgets.QComboBox(parent=Form)
        self.combo_dep.setGeometry(QtCore.QRect(100, 60, 401, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.combo_dep.setFont(font)
        self.combo_dep.setObjectName("combo_dep")
        self.label_9 = QtWidgets.QLabel(parent=Form)
        self.label_9.setGeometry(QtCore.QRect(10, 120, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.pos_combo = QtWidgets.QComboBox(parent=Form)
        self.pos_combo.setGeometry(QtCore.QRect(120, 120, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pos_combo.setFont(font)
        self.pos_combo.setObjectName("pos_combo")
        self.gr_name_line = QtWidgets.QLineEdit(parent=Form)
        self.gr_name_line.setGeometry(QtCore.QRect(350, 10, 1, 1))
        self.gr_name_line.setObjectName("gr_name_line")
        self.ok = QtWidgets.QPushButton(parent=Form)
        self.ok.setGeometry(QtCore.QRect(40, 170, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ok.setFont(font)
        self.ok.setObjectName("ok")
        self.no = QtWidgets.QPushButton(parent=Form)
        self.no.setGeometry(QtCore.QRect(350, 170, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.no.setFont(font)
        self.no.setObjectName("no")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить должность"))
        self.label.setText(_translate("Form", "Добавить должность"))
        self.label_8.setText(_translate("Form", "Отдел"))
        self.label_9.setText(_translate("Form", "Должность"))
        self.ok.setText(_translate("Form", "Готово"))
        self.no.setText(_translate("Form", "Отмена"))
        self.combo_dep.currentIndexChanged.connect(self.loadPos)
        self.ok.clicked.connect(self.addPosInGroup_BD)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
