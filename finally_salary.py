from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd


class Ui_Form_Finally(object):
    def SaveFile(self):
        columnHeaders = []
        for j in range(self.final_salary_dep.columnCount()):
            columnHeaders.append(self.final_salary_dep.horizontalHeaderItem(j).text())
        df = pd.DataFrame(columns=columnHeaders)
        for row in range(self.final_salary_dep.rowCount()):
            for col in range(self.final_salary_dep.columnCount()):
                df.at[row, columnHeaders[col]] = self.final_salary_dep.item(
                    row, col
                ).text()
        df.to_excel("effect_contract_{}.xlsx".format(self.dep_line.text()), index=False)
        print("Файл экспортирован")

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1106, 883)
        self.dep_line = QtWidgets.QLineEdit(parent=Form)
        self.dep_line.setGeometry(QtCore.QRect(100, 70, 1, 1))
        self.dep_line.setObjectName("dep_line")
        self.final_salary_dep = QtWidgets.QTableWidget(parent=Form)
        self.final_salary_dep.setGeometry(QtCore.QRect(20, 60, 1081, 731))
        self.final_salary_dep.setObjectName("final_salary_dep")
        self.final_salary_dep.setColumnCount(0)
        self.final_salary_dep.setRowCount(0)
        self.save_xlsx_file = QtWidgets.QPushButton(parent=Form)
        self.save_xlsx_file.setGeometry(QtCore.QRect(20, 10, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.save_xlsx_file.setFont(font)
        self.save_xlsx_file.setObjectName("save_xlsx_file")
        self.destroy_wind = QtWidgets.QPushButton(parent=Form)
        self.destroy_wind.setGeometry(QtCore.QRect(980, 10, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.destroy_wind.setFont(font)
        self.destroy_wind.setObjectName("destroy_wind")
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.save_xlsx_file.clicked.connect(self.SaveFile)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Итоговая зарплата отдела"))
        self.save_xlsx_file.setText(_translate("Form", "Скачать xlsx файл"))
        self.destroy_wind.setText(_translate("Form", "Выйти"))
        self.dep_line.setVisible(False)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form_Finally()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
