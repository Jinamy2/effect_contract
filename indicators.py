from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd
from add_pos_in_group import Ui_Form


class Ui_Form_Ind(object):
    def showWindow(self):
        self.window = QWidget()
        self.ui = Ui_Form()
        self.ui.setupUi(self.window)
        self.window.show()
        self.ui.loadDep()
        self.ui.loadPos()
        name_gr = self.ind_group_line.text()
        self.ui.gr_name_line.setText(name_gr)
        self.ui.ok.clicked.connect(self.window.close)
        self.ui.ok.clicked.connect(self.loadPosIndGroup)
        self.ui.no.clicked.connect(self.window.close)

    def startHiddenInd(self):
        self.ind_input_line.setVisible(False)
        self.add_new_ind_ok.setVisible(False)
        self.add_new_ind_no.setVisible(False)
        self.ind_position.setVisible(False)
        self.del_pos_out_group.setVisible(False)
        self.edit_ind_table_ok.setVisible(False)
        self.indicators_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.pos_grouptable.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.add_pos_in_group.setVisible(False)

    def setAddIndTrue(self):
        self.add_new_ind_ok.setVisible(True)
        self.ind_input_line.setVisible(True)
        self.add_new_ind_no.setVisible(True)

    def setAddIndFalse(self):
        self.add_new_ind_no.setVisible(False)
        self.ind_input_line.setVisible(False)
        self.add_new_ind_ok.setVisible(False)

    def loadInd(self):
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
        name_group = self.ind_group_line.text()
        cursor.execute(
            "SELECT id,name_ind from indicators WHERE position_group in (select id from position_group where name_group = '{}')".format(
                name_group
            )
        )
        indicators = cursor.fetchall()
        self.indicators_table.setRowCount(0)
        self.indicators_table.setColumnCount(2)
        self.indicators_table.hideColumn(0)
        self.indicators_table.setHorizontalHeaderLabels(["id", "Название показателя"])
        for row_number, row_data in enumerate(indicators):
            self.indicators_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.indicators_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.indicators_table.resizeColumnsToContents()
        connection.close()

    def addIndInBD(self):
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
        name_group = self.ind_group_line.text()
        name_ind = self.ind_input_line.text()
        cursor.execute(
            "INSERT INTO `indicators` (`id`, `name_ind`, `position_group`) VALUES (NULL, '{}', (select id from position_group where name_group = '{}'));".format(
                name_ind, name_group
            )
        )
        connection.commit()
        self.loadInd()
        self.setAddIndFalse()
        self.ind_input_line.setText("")
        connection.close()

    def setEditIndTrue(self):
        self.indicators_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
        )
        self.edit_ind_table_ok.setVisible(True)

    def editInd(self):
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
        for i in range(self.indicators_table.rowCount()):
            id = self.indicators_table.item(i, 0).text()
            name_ind = self.indicators_table.item(i, 1).text()
            cursor.execute(
                "UPDATE `indicators` SET `name_ind` = '{}' WHERE `indicators`.`id` = {};".format(
                    name_ind, id
                )
            )
            connection.commit()
        self.indicators_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.edit_ind_table_ok.setVisible(False)
        self.loadInd()
        connection.close()

    def itemIndClicked(self):
        self.ind_position.setVisible(True)

    def delInd(self):
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
        row = self.indicators_table.currentRow()
        id = self.indicators_table.item(row, 0).text()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM indicators WHERE id = {}".format(id))
        connection.commit()
        self.loadInd()
        self.noIndPos()
        connection.close()

    def noIndPos(self):
        self.ind_position.setVisible(False)

    def loadPosIndGroup(self):
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
        name_group = self.ind_group_line.text()
        cursor.execute(
            "SELECT pos_and_group.id ,department.name_dep,position.name_pos from position join pos_and_group on position.id=pos_and_group.id_pos left join department on department.id_dep=position.department WHERE pos_and_group.id_group in (select id from position_group where name_group = '{}')".format(
                name_group
            )
        )
        positions = cursor.fetchall()
        self.pos_grouptable.setRowCount(0)
        self.pos_grouptable.setColumnCount(3)
        self.pos_grouptable.hideColumn(0)
        self.pos_grouptable.setHorizontalHeaderLabels(
            ["id", "Название отдела", "Название должности"]
        )
        for row_number, row_data in enumerate(positions):
            self.pos_grouptable.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.pos_grouptable.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.pos_grouptable.resizeColumnsToContents()
        connection.close()

    def itemPosClicked(self):
        self.del_pos_out_group.setVisible(True)

    def delPos(self):
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
        row = self.pos_grouptable.currentRow()
        id = self.pos_grouptable.item(row, 0).text()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM pos_and_group WHERE id = {}".format(id))
        connection.commit()
        self.loadPosIndGroup()
        self.noIndPos()
        connection.close()

    def noIndPos(self):
        self.del_pos_out_group.setVisible(False)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1106, 883)
        self.indicators_table = QtWidgets.QTableWidget(parent=Form)
        self.indicators_table.setGeometry(QtCore.QRect(20, 110, 651, 491))
        self.indicators_table.setObjectName("indicators_table")
        self.indicators_table.setColumnCount(0)
        self.indicators_table.setRowCount(0)
        self.create_new_ind = QtWidgets.QPushButton(parent=Form)
        self.create_new_ind.setGeometry(QtCore.QRect(20, 10, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.create_new_ind.setFont(font)
        self.create_new_ind.setObjectName("create_new_ind")
        self.ind_input_line = QtWidgets.QLineEdit(parent=Form)
        self.ind_input_line.setGeometry(QtCore.QRect(350, 10, 401, 41))
        self.ind_input_line.setObjectName("ind_input_line")
        self.ind_group_line = QtWidgets.QLineEdit(parent=Form)
        self.ind_group_line.setGeometry(QtCore.QRect(350, 10, 1, 1))
        self.ind_group_line.setObjectName("ind_group_line")
        self.add_new_ind_ok = QtWidgets.QPushButton(parent=Form)
        self.add_new_ind_ok.setGeometry(QtCore.QRect(760, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_ind_ok.setFont(font)
        self.add_new_ind_ok.setObjectName("add_new_ind_ok")
        self.add_pos_in_group = QtWidgets.QPushButton(parent=Form)
        self.add_pos_in_group.setGeometry(QtCore.QRect(710, 610, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_pos_in_group.setFont(font)
        self.add_pos_in_group.setObjectName("add_pos_in_group")
        self.add_new_ind_no = QtWidgets.QPushButton(parent=Form)
        self.add_new_ind_no.setGeometry(QtCore.QRect(870, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_ind_no.setFont(font)
        self.add_new_ind_no.setObjectName("add_new_ind_no")
        self.edit_ind_table_true = QtWidgets.QPushButton(parent=Form)
        self.edit_ind_table_true.setGeometry(QtCore.QRect(20, 60, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_ind_table_true.setFont(font)
        self.edit_ind_table_true.setObjectName("edit_ind_table_true")
        self.ind_position = QtWidgets.QPushButton(parent=Form)
        self.ind_position.setGeometry(QtCore.QRect(350, 60, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ind_position.setFont(font)
        self.ind_position.setObjectName("ind_position")
        self.edit_ind_table_ok = QtWidgets.QPushButton(parent=Form)
        self.edit_ind_table_ok.setGeometry(QtCore.QRect(20, 610, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_ind_table_ok.setFont(font)
        self.edit_ind_table_ok.setObjectName("edit_ind_table_ok")
        self.pos_grouptable = QtWidgets.QTableWidget(parent=Form)
        self.pos_grouptable.setGeometry(QtCore.QRect(710, 110, 381, 491))
        self.pos_grouptable.setObjectName("pos_grouptable")
        self.pos_grouptable.setColumnCount(0)
        self.pos_grouptable.setRowCount(0)
        self.add_pos_to_group = QtWidgets.QPushButton(parent=Form)
        self.add_pos_to_group.setGeometry(QtCore.QRect(710, 60, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_pos_to_group.setFont(font)
        self.add_pos_to_group.setObjectName("add_pos_to_group")
        self.del_pos_out_group = QtWidgets.QPushButton(parent=Form)
        self.del_pos_out_group.setGeometry(QtCore.QRect(910, 60, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_pos_out_group.setFont(font)
        self.del_pos_out_group.setObjectName("del_pos_out_group")
        self.destroy_wind = QtWidgets.QPushButton(parent=Form)
        self.destroy_wind.setGeometry(QtCore.QRect(980, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.destroy_wind.setFont(font)
        self.destroy_wind.setObjectName("destroy_wind")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.create_new_ind.clicked.connect(self.setAddIndTrue)
        self.add_new_ind_no.clicked.connect(self.setAddIndFalse)
        self.add_new_ind_ok.clicked.connect(self.addIndInBD)
        self.edit_ind_table_true.clicked.connect(self.setEditIndTrue)
        self.edit_ind_table_ok.clicked.connect(self.editInd)
        self.indicators_table.itemClicked.connect(self.itemIndClicked)
        self.ind_position.clicked.connect(self.delInd)
        self.add_pos_to_group.clicked.connect(self.showWindow)
        self.add_pos_to_group.clicked.connect(self.loadPosIndGroup)
        self.pos_grouptable.itemClicked.connect(self.itemPosClicked)
        self.del_pos_out_group.clicked.connect(self.delPos)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Показатели"))
        self.create_new_ind.setText(_translate("Form", "Создать показатель"))
        self.add_new_ind_ok.setText(_translate("Form", "OK"))
        self.add_new_ind_no.setText(_translate("Form", "Отмена"))
        self.edit_ind_table_true.setText(_translate("Form", "Редактировать"))
        self.ind_position.setText(_translate("Form", "Удалить показатель"))
        self.edit_ind_table_ok.setText(_translate("Form", "Готово"))
        self.add_pos_in_group.setText(_translate("Form", "Готово"))
        self.add_pos_to_group.setText(_translate("Form", "Добавить"))
        self.del_pos_out_group.setText(_translate("Form", "Удалить"))
        self.destroy_wind.setText(_translate("Form", "Выйти"))
        self.ind_group_line.setVisible(False)
        self.startHiddenInd()
        self.loadPosIndGroup()
        self.loadInd()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Ind()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
