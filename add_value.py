from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd


class Ui_Form_Add_Ind(object):
    def loadStaffI(self):
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
        name_group = self.ind_group_input_line.text()
        cursor.execute(
            "select CONCAT(fam, ' ', name, ' ',otch) from staff where staff.position in (select position.id from position where  position.department in (select department.id_dep from department where department.name_dep = '{}')) and staff.position in (select pos_and_group.id_pos from pos_and_group where pos_and_group.id_group in (select position_group.id from position_group where position_group.name_group = '{}'))".format(
                name_dep, name_group
            )
        )
        result = cursor.fetchall()
        self.staff_indicators_table.setRowCount(0)
        self.staff_indicators_table.setColumnCount(1)
        for row_number, row_data in enumerate(result):
            self.staff_indicators_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.staff_indicators_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        name_column = ["Фио", "Коэф. сотрудника"]
        self.staff_indicators_table.insertColumn(1)
        cursor.execute(
            "select count(*) as count from indicators where position_group in (select id from position_group where name_group = '{}')".format(
                name_group
            )
        )
        count = cursor.fetchall()
        count_i = int(count[0]["count"])
        cursor.execute(
            "select name_ind from indicators where position_group in (select id from position_group where name_group = '{}')".format(
                name_group
            )
        )
        indicators = cursor.fetchall()
        if count_i != 0:
            for i in range(count_i):
                self.staff_indicators_table.insertColumn(
                    self.staff_indicators_table.columnCount()
                )
                name_column.append(indicators[i]["name_ind"])
        self.staff_indicators_table.setHorizontalHeaderLabels(name_column)
        self.staff_indicators_table.resizeColumnsToContents()
        connection.close()
        self.loadKoaf()

    def loadKoaf(self):
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
        for i in range(self.staff_indicators_table.rowCount()):
            staff = self.staff_indicators_table.item(i, 0).text()
            name_dep = self.dep_line.text()
            name_group = self.ind_group_input_line.text()
            cursor.execute(
                "select name_staff from fin_staff_salary where name_staff in (select staff.id from staff where CONCAT(staff.fam, ' ', staff.name, ' ',staff.otch)='{}' and staff.position in (select position.id from position where position.department in (select department.id_dep from department where name_dep = '{}') and position.id in (select pos_and_group.id_pos from pos_and_group where pos_and_group.id_group in (SELECT position_group.id FROM position_group WHERE position_group.name_group = '{}'))))".format(
                    staff, name_dep, name_group
                )
            )
            if cursor.rowcount == 0:
                self.staff_indicators_table.item(i, 0).setBackground(
                    QtGui.QColor(255, 255, 0)
                )
            cursor.execute(
                "select koaf from fin_staff_salary where name_staff in (select staff.id from staff where CONCAT(staff.fam, ' ', staff.name, ' ',staff.otch)='{}' and staff.position in (select position.id from position where position.department in (select department.id_dep from department where name_dep = '{}') and position.id in (select pos_and_group.id_pos from pos_and_group where pos_and_group.id_group in (SELECT position_group.id FROM position_group WHERE position_group.name_group = '{}'))))".format(
                    staff, name_dep, name_group
                )
            )
            koaf = cursor.fetchall()
            if cursor.rowcount != 0:
                self.staff_indicators_table.setItem(
                    i, 1, QTableWidgetItem(str(koaf[0]["koaf"]))
                )
            else:
                self.staff_indicators_table.item(i, 0).setBackground(
                    QtGui.QColor(255, 255, 0)
                )
            for j in range(2, self.staff_indicators_table.columnCount()):
                cursor.execute(
                    "select name_ind from indicators where position_group in (select id from position_group where name_group = '{}')".format(
                        name_group
                    )
                )
                indicators = cursor.fetchall()
                indic = indicators[j - 2]["name_ind"]
                staff = self.staff_indicators_table.item(i, 0).text()
                name_dep = self.dep_line.text()
                name_group = self.ind_group_input_line.text()
                cursor.execute(
                    "select value from indicators_values where name_ind in (select indicators.id from indicators where indicators.name_ind = '{}' and indicators.position_group in (select position_group.id from position_group where name_group = '{}')) and staff in (select staff.id from staff where staff.position in (select pos_and_group.id_pos from pos_and_group where pos_and_group.id_group in (select position_group.id from position_group where name_group = '{}') and pos_and_group.id_pos in (select position.id from position where position.department in (select id_dep from department where name_dep = '{}'))) and CONCAT(staff.fam, ' ', staff.name, ' ',staff.otch) LIKE '{}');".format(
                        str(indic), name_group, name_group, name_dep, staff
                    )
                )
                value_ind = cursor.fetchall()
                if cursor.rowcount != 0:
                    self.staff_indicators_table.setItem(
                        i, j, QTableWidgetItem(str(value_ind[0]["value"]))
                    )
                else:
                    self.staff_indicators_table.item(i, 0).setBackground(
                        QtGui.QColor(255, 255, 0)
                    )
        connection.close()

    def InsertIndStaff(self):
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
        name_dep = self.dep_line.text()
        name_group = self.ind_group_input_line.text()
        countColumn = self.staff_indicators_table.columnCount()
        countRow = self.staff_indicators_table.rowCount()
        sum = 0
        ind = []
        cursor = connection.cursor()
        cursor.execute(
            "select count(*) as count from indicators where position_group in (select id from position_group where name_group = '{}')".format(
                name_group
            )
        )
        count = cursor.fetchall()
        count_i = int(count[0]["count"])
        for row in range(0, countRow):
            staff = self.staff_indicators_table.item(row, 0).text()
            cursor.execute(
                "select position.name_pos as name from position where position.id in (select position from staff where position in (select id from position where position.department in (select id_dep from department where name_dep = '{}')) and position in (select pos_and_group.id_pos from pos_and_group where pos_and_group.id_group in (select position_group.id from position_group where name_group = '{}')) and CONCAT(staff.fam, ' ', staff.name, ' ',staff.otch) LIKE '{}')".format(
                    name_dep, name_group, staff
                )
            )
            res = cursor.fetchall()
            pos = res[0]["name"]
            for column in range(2, countColumn):
                cursor.execute(
                    "select name_ind from indicators where position_group in (select id from position_group where name_group = '{}')".format(
                        name_group
                    )
                )
                indicators = cursor.fetchall()
                indic = indicators[column - 2]["name_ind"]
                value = self.staff_indicators_table.item(row, column).text()
                cursor.execute(
                    "DELETE FROM indicators_values WHERE indicators_values.name_ind in (Select id from indicators where name_ind ='{}' and position_group in (select id from position_group where name_group = '{}')) AND indicators_values.staff in (select id from staff where CONCAT(fam, ' ', name, ' ',otch) = '{}' and position in (select id from position where position.name_pos = '{}'))".format(
                        str(indic), name_group, staff, pos
                    )
                )
                connection.commit()
                cursor.execute(
                    "INSERT INTO `indicators_values` (`id`, `name_ind`, `staff`, `value`) VALUES (NULL, (Select id from indicators where name_ind ='{}'and position_group in (select id from position_group where name_group = '{}') and position_group in (select id_group from pos_and_group where id_pos in (select id from position where position.department in (select department.id_dep from department where department.name_dep = '{}')))), (select id from staff where CONCAT(fam, ' ', name, ' ',otch) = '{}' and position in (select id from position where position.name_pos = '{}' and position.department in (select department.id_dep from department where department.name_dep = '{}'))), '{}');".format(
                        str(indic), name_group, name_dep, staff, pos, name_dep, value
                    )
                )
                connection.commit()
                ind.append(self.staff_indicators_table.item(row, column).text())
                sum += int(ind[row])
            print(sum)
            itog = round(sum / (count_i * 20), 1)
            sum = 0
            koaf_by_ruk = float(self.staff_indicators_table.item(row, 1).text())
            koaf_by_ind = float(itog)
            cursor.execute(
                "DELETE FROM fin_staff_salary where name_staff in (select id from staff where CONCAT(fam, ' ', name, ' ',otch) = '{}' and position in (select id from position where position.name_pos = '{}')) and name_dep in  (select id_dep from department where name_dep = '{}');".format(
                    staff, pos, name_dep
                )
            )
            connection.commit()
            cursor.execute(
                "select position.salary as salary from position where position.id in (select position from staff where position in (select id from position where position.department in (select id_dep from department where name_dep = '{}')) and position in (select pos_and_group.id_pos from pos_and_group where pos_and_group.id_group in (select position_group.id from position_group where name_group = '{}')) and CONCAT(staff.fam, ' ', staff.name, ' ',staff.otch) LIKE '{}')".format(
                    name_dep, name_group, staff
                )
            )
            sal = cursor.fetchall()
            current_salary_pos = float(sal[0]["salary"]) * koaf_by_ind * koaf_by_ruk
            cursor.execute(
                "INSERT INTO `fin_staff_salary` (`id`, `name_staff`, `name_dep`, `koaf`, `koaf_ind`, `salary_with_koaf_ind`, `finally_salary`) VALUES (NULL, (select id from staff where CONCAT(fam, ' ', name, ' ',otch) = '{}' and position in (select id from position where position.name_pos = '{}' and position.department in (select department.id_dep from department where department.name_dep = '{}'))) , (select id_dep from department where name_dep = '{}'), {}, {}, {}, NULL);".format(
                    staff,
                    pos,
                    name_dep,
                    name_dep,
                    koaf_by_ruk,
                    koaf_by_ind,
                    current_salary_pos,
                )
            )
            connection.commit()
            print("вставил человека")
        cursor.execute(
            "SELECT COUNT(*) as count FROM `fin_staff_salary` where name_dep in (select department.id_dep from department where department.name_dep = '{}');".format(
                name_dep
            )
        )
        count = cursor.fetchall()
        fin = count[0]["count"]
        self.fin_line.setText(str(fin))
        connection.commit()
        connection.close()
        self.loadStaffI()
        self.loadKoaf()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1106, 883)
        self.staff_indicators_table = QtWidgets.QTableWidget(parent=Form)
        self.staff_indicators_table.setGeometry(QtCore.QRect(20, 60, 1081, 731))
        self.staff_indicators_table.setObjectName("staff_indicators_table")
        self.staff_indicators_table.setColumnCount(0)
        self.staff_indicators_table.setRowCount(0)
        self.add_staff_int = QtWidgets.QPushButton(parent=Form)
        self.add_staff_int.setGeometry(QtCore.QRect(20, 10, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_staff_int.setFont(font)
        self.add_staff_int.setObjectName("add_staff_int")
        self.ind_group_input_line = QtWidgets.QLineEdit(parent=Form)
        self.ind_group_input_line.setGeometry(QtCore.QRect(340, 70, 1, 1))
        self.ind_group_input_line.setObjectName("ind_group_input_line")
        self.dep_line = QtWidgets.QLineEdit(parent=Form)
        self.dep_line.setGeometry(QtCore.QRect(340, 70, 1, 1))
        self.dep_line.setObjectName("dep_line")
        self.fin_line = QtWidgets.QLineEdit(parent=Form)
        self.fin_line.setGeometry(QtCore.QRect(340, 70, 1, 1))
        self.fin_line.setObjectName("fin_line")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.add_staff_int.clicked.connect(self.InsertIndStaff)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_staff_int.setText(_translate("Form", "Занести значения показателей"))
        self.ind_group_input_line.setVisible(False)
        self.dep_line.setVisible(False)
        self.fin_line.setVisible(False)
        self.loadStaffI()
        self.loadKoaf()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Add_Ind()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
