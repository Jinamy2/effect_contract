# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


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
        self.comboBox.addItem("")
        self.comboBox.addItem("")
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
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
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
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.TabWidget.addTab(self.salary, "")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action_2 = QtGui.QAction(parent=mainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=mainWindow)
        self.action_3.setObjectName("action_3")

        self.retranslateUi(mainWindow)
        self.TabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Эффективный контракт"))
        self.label.setText(_translate("mainWindow", "Отдел"))
        self.comboBox.setItemText(0, _translate("mainWindow", "Сопровождение инф. систем"))
        self.comboBox.setItemText(1, _translate("mainWindow", "Лаборатория"))
        self.label_2.setText(_translate("mainWindow", "Сумма"))
        self.pushButton.setText(_translate("mainWindow", "Изменить сумму"))
        self.pushButton_2.setText(_translate("mainWindow", "Добавить строку"))
        self.pushButton_3.setText(_translate("mainWindow", "Удалить строку"))
        self.pushButton_4.setText(_translate("mainWindow", "Обновить данные"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.staff), _translate("mainWindow", "Tab 1"))
        self.label_3.setText(_translate("mainWindow", "Должность"))
        self.comboBox_2.setItemText(0, _translate("mainWindow", "Сопровождение инф. систем"))
        self.comboBox_2.setItemText(1, _translate("mainWindow", "Лаборатория"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.indicators), _translate("mainWindow", "Tab 2"))
        self.label_4.setText(_translate("mainWindow", "Сотрудник"))
        self.comboBox_3.setItemText(0, _translate("mainWindow", "Сопровождение инф. систем"))
        self.comboBox_3.setItemText(1, _translate("mainWindow", "Лаборатория"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.salary), _translate("mainWindow", "Page"))
        self.action_2.setText(_translate("mainWindow", "Бюджет"))
        self.action_3.setText(_translate("mainWindow", "Сотрудники"))
