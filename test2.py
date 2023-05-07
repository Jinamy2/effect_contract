from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql

try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor,
    )
    print("Соединение успешно")
    with connection.cursor() as cursor:
        select_staff_log_query = "select count(*) as count from staff;"
        cursor.execute(select_staff_log_query)
        count_staff = cursor.fetchall()
        count_s = count_staff[0]["count"]

except Exception as ex:
    print("Соединение прервано")
    print(ex)


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.TabWidget.setGeometry(QtCore.QRect(0, 10, 801, 591))
        self.TabWidget.setObjectName("TabWidget")
        self.staff = QtWidgets.QWidget()
        self.staff.setAccessibleName("")
        self.staff.setObjectName("staff")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.staff)
        self.tableWidget.setGeometry(QtCore.QRect(10, 170, 771, 331))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(parent=self.staff)
        self.label.setGeometry(QtCore.QRect(30, 30, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(parent=self.staff)
        self.comboBox.setGeometry(QtCore.QRect(130, 35, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox.setFont(font)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.label_2 = QtWidgets.QLabel(parent=self.staff)
        self.label_2.setGeometry(QtCore.QRect(470, 30, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.staff)
        self.lineEdit.setGeometry(QtCore.QRect(560, 35, 161, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(parent=self.staff)
        self.pushButton.setGeometry(QtCore.QRect(560, 80, 161, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.staff)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 120, 161, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.staff)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 120, 161, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.staff)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 120, 161, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.TabWidget.addTab(self.staff, "")
        self.indicators = QtWidgets.QWidget()
        self.indicators.setObjectName("indicators")
        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.indicators)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 200, 771, 331))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.label_3 = QtWidgets.QLabel(parent=self.indicators)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.indicators)
        self.comboBox_2.setGeometry(QtCore.QRect(190, 35, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName("comboBox_2")
        self.TabWidget.addTab(self.indicators, "")
        self.salary = QtWidgets.QWidget()
        self.salary.setObjectName("salary")
        self.tableWidget_3 = QtWidgets.QTableWidget(parent=self.salary)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 200, 771, 331))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.label_4 = QtWidgets.QLabel(parent=self.salary)
        self.label_4.setGeometry(QtCore.QRect(30, 30, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.comboBox_3 = QtWidgets.QComboBox(parent=self.salary)
        self.comboBox_3.setGeometry(QtCore.QRect(180, 35, 300, 25))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setObjectName("comboBox_3")
        self.TabWidget.addTab(self.salary, "")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action_2 = QtGui.QAction(parent=mainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=mainWindow)
        self.action_3.setObjectName("action_3")

        self.comboBox.currentIndexChanged.connect(self.set_money_dep)
        self.comboBox.currentIndexChanged.connect(self.LoadStuff)
        self.comboBox.currentIndexChanged.connect(self.LoadInd)
        self.comboBox_2.currentIndexChanged.connect(self.LoadInd)
        self.comboBox_2.currentIndexChanged.connect(self.current_staff)
        self.pushButton_2.clicked.connect(self.DropRow)
        self.pushButton.clicked.connect(self.update_money)
        self.retranslateUi(mainWindow)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def DropRow(self):
        cur_row = self.tableWidget.currentRow()
        log = self.tableWidget.item(cur_row, 4).text()
        cursor = connection.cursor()
        cursor.execute("delete from staff where login = '{}'".format(log))
        connection.commit()
        self.tableWidget.removeRow(cur_row)

    def update_money(self):
        cur_sum = self.lineEdit.text()
        cur_dep = self.comboBox.currentText()
        money_dep_query = (
            " UPDATE department SET money = {} WHERE name_dep='{}'".format(
                cur_sum, cur_dep
            )
        )
        cursor = connection.cursor()
        cursor.execute(money_dep_query)
        connection.commit()

    def current_staff(self):
        name_posithion = self.comboBox_2.currentText()
        staff_name_query = "select CONCAT(fam, ' ', name, ' ',otch) as name_staff from staff join position on position.id=staff.position where name_pos = '{}'".format(
            name_posithion
        )
        cursor = connection.cursor()
        cursor.execute(staff_name_query)
        staff_name = cursor.fetchall()
        print(staff_name)
        if cursor.rowcount == 0:
            self.comboBox_3.addItem("")
            self.comboBox_3.setItemText(0, "Сотрудников нет")
        else:
            for row_number, data in enumerate(staff_name):
                self.comboBox_3.addItem("")
                self.comboBox_3.setItemText(row_number, data["name_staff"])

    def set_money_dep(self):
        dep = self.comboBox.currentText()
        money_dep_query = "select money from department where name_dep = '{}'".format(
            dep
        )
        cursor = connection.cursor()
        cursor.execute(money_dep_query)
        money_d = cursor.fetchall()
        for row in money_d:
            self.lineEdit.setText(str(row["money"]))

    def LoadStuff(self):
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor,
        )
        cursor = connection.cursor()
        dep = self.comboBox.currentText()
        cursor.execute(
            "select fam,name,otch,position.name_pos,login from staff join position on staff.position = position.id LEFT JOIN department on department.id_dep=position.department where department.name_dep = '{}'".format(
                dep
            )
        )
        result = cursor.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.tableWidget.resizeColumnsToContents()

    def LoadInd(self):
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor,
        )
        cursor = connection.cursor()
        dep = self.comboBox.currentText()
        pos = self.comboBox_2.currentText()
        cursor.execute(
            "select indicators.name_ind, position.name_pos from indicators join position on position.id=indicators.position left join department on department.id_dep=position.department where department.name_dep = '{}' and position.name_pos = '{}'".format(
                dep, pos
            )
        )
        result = cursor.fetchall()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(2)
        for row_number, row_data in enumerate(result):
            self.tableWidget_2.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.tableWidget_2.resizeColumnsToContents()

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Эффективный контракт"))
        self.label.setText(_translate("mainWindow", "Отдел"))
        dep_qury = "select * from department"
        cursor = connection.cursor()
        cursor.execute(dep_qury)
        departmens = cursor.fetchall()
        for row_number, data in enumerate(departmens):
            self.comboBox.addItem("")
            self.comboBox.setItemText(
                row_number, _translate("mainWindow", data["name_dep"])
            )
        self.label_2.setText(_translate("mainWindow", "Сумма"))
        self.label_3.setText(_translate("mainWindow", "Должность"))
        self.label_4.setText(_translate("mainWindow", "Сотрудник"))
        self.pushButton.setText(_translate("mainWindow", "Изменить сумму"))
        self.pushButton_2.setText(_translate("mainWindow", "Удалить сотрудника"))
        self.TabWidget.setTabText(
            self.TabWidget.indexOf(self.staff), _translate("mainWindow", "Сотрудники")
        )
        self.TabWidget.setTabText(
            self.TabWidget.indexOf(self.indicators),
            _translate("mainWindow", "Показатели"),
        )
        self.TabWidget.setTabText(
            self.TabWidget.indexOf(self.salary), _translate("mainWindow", "Расчет ЗП")
        )
        self.action_2.setText(_translate("mainWindow", "Бюджет"))
        self.action_3.setText(_translate("mainWindow", "Сотрудники"))
        cursor = connection.cursor()
        cursor.execute("select name_dep from department where id_dep=1")
        start_dep = cursor.fetchall()
        dep_name = start_dep[0]["name_dep"]
        money_query = "select money from department where name_dep = '{}'".format(
            dep_name
        )
        name_pos_query = "select name_pos from position join department on position.department=department.id_dep where department.name_dep = '{}'".format(
            dep_name
        )
        cursor.execute(name_pos_query)
        position_name = cursor.fetchall()
        for row_number, data in enumerate(position_name):
            self.comboBox_2.addItem("")
            self.comboBox_2.setItemText(
                row_number, _translate("mainWindow", data["name_pos"])
            )
        name_posithion = self.comboBox_2.currentText()
        staff_name_query = "select CONCAT(fam, ' ', name, ' ',otch) as name_staff from staff join position on position.id=staff.position where name_pos = '{}'".format(
            name_posithion
        )
        cursor.execute(staff_name_query)
        staff_name = cursor.fetchall()
        if cursor.rowcount == 0:
            self.comboBox_3.addItem("")
            self.comboBox_3.setItemText(0, "Сотрудников нет")
        else:
            for row_number, data in enumerate(staff_name):
                self.comboBox_3.addItem("")
                self.comboBox_3.setItemText(row_number, data["name_staff"])
        cursor = connection.cursor()
        cursor.execute(money_query)
        money_dep = cursor.fetchall()
        dep_m = money_dep[0]["money"]
        cursor = connection.cursor()
        cursor.execute(
            "select fam,name,otch,position.name_pos,login from staff join position on staff.position = position.id LEFT JOIN department on department.id_dep=position.department where department.name_dep = '{}'".format(
                dep_name
            )
        )
        result = cursor.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.tableWidget.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.tableWidget.resizeColumnsToContents()
        cursor = connection.cursor()
        cursor.execute(
            "select indicators.name_ind, position.name_pos from indicators join position on position.id=indicators.position left join department on department.id_dep=position.department where department.name_dep = '{}'".format(
                dep_name
            )
        )
        result = cursor.fetchall()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(2)
        for row_number, row_data in enumerate(result):
            self.tableWidget_2.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.tableWidget_2.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.tableWidget_2.resizeColumnsToContents()
        self.lineEdit.setText(str(dep_m))
        self.tableWidget.hideColumn(4)
        self.tableWidget_2.hideColumn(1)
        self.LoadStuff()
        self.LoadInd()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
