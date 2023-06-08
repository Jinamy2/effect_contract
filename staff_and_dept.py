from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd
from add_staff import Ui_Add_Staff


class Ui_Form_Staff(object):
    def showAddStaffWindow(self):
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
        self.window = QWidget()
        self.ui = Ui_Add_Staff()
        self.ui.setupUi(self.window)
        self.window.show()
        dep_name = self.dep_line.text()
        self.ui.dep_line.setText(dep_name)
        self.ui.pos_comboBox.clear()
        name_pos_query = "select name_pos from position where department in (select id_dep from department where name_dep = '{}')".format(
            dep_name
        )
        cursor = connection.cursor()
        cursor.execute(name_pos_query)
        position_name = cursor.fetchall()
        for row_number, data in enumerate(position_name):
            self.ui.pos_comboBox.addItem("")
            self.ui.pos_comboBox.setItemText(row_number, data["name_pos"])
        self.ui.add_staff_in_bd.clicked.connect(self.window.close)
        self.ui.add_staff_in_bd.clicked.connect(self.loadStaff)
        self.ui.hide_staff_in_bd.clicked.connect(self.window.close)
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
        cursor = connection.cursor()
        name_dep = self.dep_line.text()
        cursor.execute(
            "SELECT * FROM `position` WHERE department in (select id_dep from department where name_dep = '{}') ".format(
                name_dep
            )
        )
        position = cursor.fetchall()
        self.position_table.setRowCount(0)
        self.position_table.setColumnCount(3)
        self.position_table.hideColumn(0)
        self.position_table.hideColumn(2)
        self.position_table.setHorizontalHeaderLabels(
            ["id", "Название должности", "Оклад"]
        )
        for row_number, row_data in enumerate(position):
            self.position_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.position_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.position_table.resizeColumnsToContents()
        connection.close()

    def setAddPosTrue(self):
        self.add_new_pos_ok.setVisible(True)
        self.pos_input_line.setVisible(True)
        self.add_new_pos_no.setVisible(True)

    def setAddPosFalse(self):
        self.add_new_pos_ok.setVisible(False)
        self.pos_input_line.setVisible(False)
        self.add_new_pos_no.setVisible(False)

    def addPosToBD(self):
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
        name_dep = self.dep_line.text()
        name_pos = self.pos_input_line.text()
        cursor.execute(
            "INSERT INTO `position` (`id`, `name_pos`, `salary`, `department`) VALUES (NULL, '{}', '0', (select id_dep from department where name_dep = '{}'));".format(
                name_pos, name_dep
            )
        )
        connection.commit()
        connection.close()
        self.loadPos()
        self.setAddPosFalse()

    def setEditPosTrue(self):
        self.position_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
        )
        self.edit_pos_table_ok.setVisible(True)

    def editPos(self):
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
        for i in range(self.position_table.rowCount()):
            id = self.position_table.item(i, 0).text()
            name_pos = self.position_table.item(i, 1).text()
            cursor.execute(
                "UPDATE position SET name_pos = '{}' WHERE position.id = {};".format(
                    name_pos, id
                )
            )
            connection.commit()
        self.position_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.edit_pos_table_ok.setVisible(False)
        connection.close()
        self.loadPos()

    def itemPosClicked(self):
        self.del_position.setVisible(True)

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
        row = self.position_table.currentRow()
        id = self.position_table.item(row, 0).text()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM position WHERE id = {}".format(id))
        connection.commit()
        connection.close()
        self.loadPos()
        self.noDelPos()

    def noDelPos(self):
        self.del_position.setVisible(False)

    def loadStaff(self):
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
        name_dep = self.dep_line.text()
        cursor.execute(
            "SELECT staff.id,CONCAT(fam, ' ', name, ' ',otch),position.name_pos,login,password from staff join position on staff.position = position.id LEFT JOIN department on department.id_dep=position.department where department.name_dep = '{}'".format(
                name_dep
            )
        )
        staff = cursor.fetchall()
        self.staff_table.setRowCount(0)
        self.staff_table.setColumnCount(7)
        self.staff_table.hideColumn(0)
        self.staff_table.hideColumn(6)
        for row_number, row_data in enumerate(staff):
            self.staff_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.staff_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.staff_table.setHorizontalHeaderLabels(
            ["id", "ФИО", "Должность", "Логин", "Пароль", "Роль"]
        )
        for row_number in range(self.staff_table.rowCount()):
            staff_id = self.staff_table.item(row_number, 0).text()
            cursor.execute(
                "select id,role from role_and_staff where staff = {}".format(staff_id)
            )
            role = cursor.fetchall()
            if cursor.rowcount != 0:
                role_line = ""
                for i in range(cursor.rowcount):
                    role_line += str(role[i]["role"]) + ","
                self.staff_table.setItem(
                    row_number, 5, QTableWidgetItem(role_line[:-1])
                )
            else:
                self.staff_table.setItem(row_number, 5, QTableWidgetItem(str(1)))
        self.staff_table.resizeColumnsToContents()
        connection.close()

    def setEditStaffTrue(self):
        self.staff_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
        )
        self.edit_staff_table_ok.setVisible(True)

    def editStaff(self):
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
        for i in range(self.staff_table.rowCount()):
            id = self.staff_table.item(i, 0).text()
            fio = self.staff_table.item(i, 1).text().split()
            fam = fio[0]
            name = fio[1]
            otch = fio[2]
            log = self.staff_table.item(i, 3).text()
            pas = self.staff_table.item(i, 4).text()
            cursor.execute(
                "UPDATE `staff` SET `fam` = '{}', `name` = '{}', `otch` = '{}', `login` = '{}', `password` = '{}' WHERE `staff`.`id` = {};".format(
                    fam, name, otch, log, pas, id
                )
            )
            connection.commit()
            roles = self.staff_table.item(i, 5).text().split(",")
            pos = self.staff_table.item(i, 2).text()
            dep = self.dep_line.text()
            staff_id = self.staff_table.item(i, 0).text()
            staff = self.staff_table.item(i, 1).text()
            cursor.execute(
                "DELETE FROM role_and_staff where staff = '{}'".format(staff_id)
            )
            connection.commit()
            for i in range(len(roles)):
                cursor.execute(
                    "INSERT INTO `role_and_staff` (`id`, `role`, `staff`) VALUES (NULL, '{}', (select id from staff where CONCAT(fam, ' ', name, ' ',otch) = '{}' and position in (select id from position where position.name_pos = '{}' and position.department in (select department.id_dep from department where department.name_dep = '{}'))));".format(
                        roles[i], staff, pos, dep
                    )
                )
                connection.commit()
        self.loadStaff()
        self.edit_staff_table_ok.setVisible(False)
        self.staff_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        connection.close()
        self.loadStaff()

    def itemStaffClicked(self):
        self.del_staff.setVisible(True)

    def delStaff(self):
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
        row = self.staff_table.currentRow()
        id = self.staff_table.item(row, 0).text()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM staff WHERE id = {}".format(id))
        connection.commit()
        connection.close()
        self.loadStaff()

    def noDelStaff(self):
        self.del_staff.setVisible(False)

    def startHidden(self):
        self.pos_input_line.setVisible(False)
        self.add_new_pos_ok.setVisible(False)
        self.add_new_pos_no.setVisible(False)
        self.dep_line.setVisible(False)
        self.del_position.setVisible(False)
        self.del_staff.setVisible(False)
        self.edit_pos_table_ok.setVisible(False)
        self.edit_staff_table_ok.setVisible(False)
        self.position_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.staff_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1106, 883)
        self.position_table = QtWidgets.QTableWidget(parent=Form)
        self.position_table.setGeometry(QtCore.QRect(20, 110, 1060, 250))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.position_table.setFont(font)
        self.position_table.setObjectName("position_table")
        self.position_table.setColumnCount(0)
        self.position_table.setRowCount(0)
        self.staff_table = QtWidgets.QTableWidget(parent=Form)
        self.staff_table.setGeometry(QtCore.QRect(20, 470, 1060, 250))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.staff_table.setFont(font)
        self.staff_table.setObjectName("staff_table")
        self.staff_table.setColumnCount(0)
        self.staff_table.setRowCount(0)
        self.create_new_pos = QtWidgets.QPushButton(parent=Form)
        self.create_new_pos.setGeometry(QtCore.QRect(20, 10, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.create_new_pos.setFont(font)
        self.create_new_pos.setObjectName("create_new_pos")
        self.pos_input_line = QtWidgets.QLineEdit(parent=Form)
        self.pos_input_line.setGeometry(QtCore.QRect(350, 10, 401, 41))
        self.pos_input_line.setObjectName("pos_input_line")
        self.dep_line = QtWidgets.QLineEdit(parent=Form)
        self.dep_line.setGeometry(QtCore.QRect(350, 10, 501, 41))
        self.dep_line.setObjectName("dep_line")
        self.add_new_pos_ok = QtWidgets.QPushButton(parent=Form)
        self.add_new_pos_ok.setGeometry(QtCore.QRect(760, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_pos_ok.setFont(font)
        self.add_new_pos_ok.setObjectName("add_new_pos_ok")
        self.add_new_pos_no = QtWidgets.QPushButton(parent=Form)
        self.add_new_pos_no.setGeometry(QtCore.QRect(870, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_pos_no.setFont(font)
        self.add_new_pos_no.setObjectName("add_new_pos_no")
        self.destroy_wind = QtWidgets.QPushButton(parent=Form)
        self.destroy_wind.setGeometry(QtCore.QRect(980, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.destroy_wind.setFont(font)
        self.destroy_wind.setObjectName("destroy_wind")
        self.edit_pos_table_true = QtWidgets.QPushButton(parent=Form)
        self.edit_pos_table_true.setGeometry(QtCore.QRect(20, 60, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_pos_table_true.setFont(font)
        self.edit_pos_table_true.setObjectName("edit_pos_table_true")
        self.del_position = QtWidgets.QPushButton(parent=Form)
        self.del_position.setGeometry(QtCore.QRect(350, 60, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_position.setFont(font)
        self.del_position.setObjectName("del_position")
        self.create_new_staff = QtWidgets.QPushButton(parent=Form)
        self.create_new_staff.setGeometry(QtCore.QRect(20, 410, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.create_new_staff.setFont(font)
        self.create_new_staff.setObjectName("create_new_staff")
        self.edit_staff_table_true = QtWidgets.QPushButton(parent=Form)
        self.edit_staff_table_true.setGeometry(QtCore.QRect(350, 410, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_staff_table_true.setFont(font)
        self.edit_staff_table_true.setObjectName("edit_staff_table_true")
        self.del_staff = QtWidgets.QPushButton(parent=Form)
        self.del_staff.setGeometry(QtCore.QRect(680, 410, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_staff.setFont(font)
        self.del_staff.setObjectName("del_staff")
        self.edit_staff_table_ok = QtWidgets.QPushButton(parent=Form)
        self.edit_staff_table_ok.setGeometry(QtCore.QRect(20, 725, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_staff_table_ok.setFont(font)
        self.edit_staff_table_ok.setObjectName("edit_staff_table_ok")
        self.edit_pos_table_ok = QtWidgets.QPushButton(parent=Form)
        self.edit_pos_table_ok.setGeometry(QtCore.QRect(20, 365, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_pos_table_ok.setFont(font)
        self.edit_pos_table_ok.setObjectName("edit_pos_table_ok")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.add_new_pos_ok.clicked.connect(self.addPosToBD)
        self.create_new_pos.clicked.connect(self.setAddPosTrue)
        self.add_new_pos_no.clicked.connect(self.setAddPosFalse)
        self.edit_pos_table_true.clicked.connect(self.setEditPosTrue)
        self.edit_pos_table_ok.clicked.connect(self.editPos)
        self.create_new_staff.clicked.connect(self.showAddStaffWindow)
        self.position_table.itemClicked.connect(self.itemPosClicked)
        self.staff_table.itemClicked.connect(self.itemStaffClicked)
        self.edit_staff_table_true.clicked.connect(self.setEditStaffTrue)
        self.edit_staff_table_ok.clicked.connect(self.editStaff)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Сотрудники и должности"))
        self.create_new_pos.setText(_translate("Form", "Создать должность"))
        self.add_new_pos_ok.setText(_translate("Form", "OK"))
        self.add_new_pos_no.setText(_translate("Form", "Отмена"))
        self.destroy_wind.setText(_translate("Form", "Выйти"))
        self.edit_pos_table_true.setText(_translate("Form", "Редактировать"))
        self.del_position.setText(_translate("Form", "Удалить должность"))
        self.create_new_staff.setText(_translate("Form", "Создать сотрудника"))
        self.edit_staff_table_true.setText(_translate("Form", "Редактировать"))
        self.del_staff.setText(_translate("Form", "Удалить сотрудника"))
        self.edit_staff_table_ok.setText(_translate("Form", "Готово"))
        self.edit_pos_table_ok.setText(_translate("Form", "Готово"))
        self.del_position.clicked.connect(self.delPos)
        self.del_staff.clicked.connect(self.delStaff)
        self.startHidden()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Staff()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
