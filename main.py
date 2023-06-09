from xml.etree.ElementTree import tostringlist
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
from config import host, user, password, db_name
import pymysql
import pandas as pd
from staff_and_dept import Ui_Form_Staff
from indicators import Ui_Form_Ind
from finally_salary import Ui_Form_Finally
from add_value import Ui_Form_Add_Ind


class Ui_MainWindow(object):
    # открытие окна для добавления нового сотрудника
    def staff_and_pos_widget(self):
        self.s_p = QWidget()
        self.ui = Ui_Form_Staff()
        self.ui.setupUi(self.s_p)
        name_dep = self.departments_table.currentItem().text()
        self.ui.dep_line.setText(name_dep)
        self.ui.loadStaff()
        self.ui.loadPos()
        self.s_p.show()
        self.ui.destroy_wind.clicked.connect(self.s_p.close)
        self.ui.destroy_wind.clicked.connect(self.loadGroupForEntered)
        self.ui.destroy_wind.clicked.connect(self.countStaffFinall)
        self.loadGroupForEntered()
        self.countStaffFinall()

    # открытие окна для добавления новых должностей в группе
    def indicators_widget(self):
        self.window = QWidget()
        self.ui = Ui_Form_Ind()
        self.ui.setupUi(self.window)
        name_ind_group = self.ind_group_table.currentItem().text()
        self.ui.ind_group_line.setText(name_ind_group)
        self.ui.loadPosIndGroup()
        self.ui.loadInd()
        self.window.show()
        self.ui.destroy_wind.clicked.connect(self.window.close)

    # открытие окна для заполнения показателей
    def finally_salary_widget(self):
        self.window = QWidget()
        self.ui = Ui_Form_Add_Ind()
        self.ui.setupUi(self.window)
        name_dep = self.comboBox_dep.currentText()
        name_ind_group = self.ind_group_table_2.currentItem().text()
        self.ui.ind_group_input_line.setText(name_ind_group)
        self.ui.dep_line.setText(name_dep)
        self.ui.loadStaffI()
        self.window.show()
        self.ui.add_staff_int.clicked.connect(self.countStaffFinall)
        self.ui.destroy_wind.clicked.connect(self.window.close)
        self.ui.destroy_wind.clicked.connect(self.countStaffFinall)

    # открытие окна с итоговым отчет о ЗП отдела
    def fin_salary_dep_widget(self):
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
        self.ui = Ui_Form_Finally()
        self.ui.setupUi(self.window)
        cursor = connection.cursor()
        dep = self.comboBox_dep.currentText()
        cursor.execute("select money from department where name_dep = '{}'".format(dep))
        sum_d = cursor.fetchall()
        sum_dep = float(sum_d[0]["money"])
        cursor.execute(
            "select sum(salary_with_koaf_ind) as summ from fin_staff_salary where name_dep in (select id_dep from department where name_dep = '{}')".format(
                dep
            )
        )
        sum = cursor.fetchall()
        sum_dep_koaf = sum[0]["summ"]
        cursor.execute(
            "UPDATE fin_staff_salary SET finally_salary= round(salary_with_koaf_ind/ {}*{},2) where name_dep in (select id_dep from department where name_dep = '{}')".format(
                float(sum_dep_koaf), sum_dep, dep
            )
        )
        connection.commit()
        cursor.execute(
            "select sum(finally_salary) as summ from fin_staff_salary where name_dep in (select id_dep from department where name_dep = '{}')".format(
                dep
            )
        )
        sum = cursor.fetchall()
        sum_itog = sum[0]["summ"]
        dif_min = sum_itog - sum_dep
        dif_more = sum_dep - sum_itog
        if dif_min > 0:
            cursor.execute(
                "UPDATE fin_staff_salary SET finally_salary = (finally_salary - {}) WHERE name_staff in (select id from staff where name_staff LIKE 'ruc%') AND (name_dep in (select id_dep from department where name_dep = '{}'));".format(
                    dif_min, dep
                )
            )
        connection.commit()
        if dif_more > 0:
            cursor.execute(
                "UPDATE fin_staff_salary SET finally_salary = finally_salary + {} WHERE name_staff in (select id from staff where name_staff LIKE 'ruc%') AND (name_dep in (select id_dep from department where name_dep = '{}'));".format(
                    dif_more, dep
                )
            )
        connection.commit()

        cursor.execute(
            "select CONCAT(staff.fam, ' ', staff.name, ' ',staff.otch), koaf,koaf_ind,salary_with_koaf_ind, finally_salary from fin_staff_salary join staff on staff.id=fin_staff_salary.name_staff where name_dep in (select id_dep from department where name_dep = '{}');".format(
                dep
            )
        )
        result = cursor.fetchall()
        self.ui.final_salary_dep.setRowCount(0)
        self.ui.final_salary_dep.setColumnCount(5)
        for row_number, row_data in enumerate(result):
            self.ui.final_salary_dep.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.ui.final_salary_dep.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        t4 = [
            "ФИО",
            "Коэф.",
            "Значение оценки",
            "Приведенный оклад",
            "Сумма на месяц руб.",
        ]
        self.ui.final_salary_dep.setHorizontalHeaderLabels(t4)
        self.ui.final_salary_dep.resizeColumnsToContents()
        self.ui.dep_line.setText(self.comboBox_dep.currentText())
        self.window.show()
        self.ui.destroy_wind.clicked.connect(self.window.close)
        connection.close()

    # работа с таблицей отделов:
    # загрузка в таблицу
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
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `department` ")
        depatments = cursor.fetchall()
        self.departments_table.setRowCount(0)
        self.departments_table.setColumnCount(3)
        self.departments_table.hideColumn(0)
        self.departments_table.hideColumn(2)
        self.departments_table.setHorizontalHeaderLabels(
            ["id", "Название отдела", "Оклад"]
        )
        for row_number, row_data in enumerate(depatments):
            self.departments_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.departments_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.departments_table.resizeColumnsToContents()
        connection.close()

    # загрузка отедлов с выпадающие списки
    def loadDepCombo(self):
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
        cursor.execute("SELECT * FROM `department` ")
        depatments = cursor.fetchall()
        self.comboBox_dep.clear()
        self.comboBox_dep_2.clear()
        for row_number, data in enumerate(depatments):
            self.comboBox_dep.addItem("")
            self.comboBox_dep.setItemText(row_number, data["name_dep"])
            self.comboBox_dep_2.addItem("")
            self.comboBox_dep_2.setItemText(row_number, data["name_dep"])
        connection.close()

    # открытие полей для создания нового подразделения
    def setAddDeptTrue(self):
        self.add_new_dep_ok.setVisible(True)
        self.dep_input_line.setVisible(True)
        self.add_new_dep_no.setVisible(True)
        self.dep_input_line.setText("")

    # закрытие полей для создания нового подразделения
    def setAddDeptFalse(self):
        self.add_new_dep_ok.setVisible(False)
        self.dep_input_line.setVisible(False)
        self.add_new_dep_no.setVisible(False)

    # добавление подразделения в БД
    def addDepToBD(self):
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
        name_dep = self.dep_input_line.text()
        cursor.execute(
            "INSERT INTO `department` (`id_dep`, `name_dep`, `money`) VALUES (NULL, '{}', '0');".format(
                name_dep
            )
        )
        connection.commit()
        connection.close()
        self.loadDep()
        self.setAddDeptFalse()

    # возможность редактировтаь поля в таблице, появление кнопки для завершения редактирования
    def setEditDepTrue(self):
        self.departments_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
        )
        self.edit_dep_table_ok.setVisible(True)

    # обновление в БД всех измененных данных в таблице
    def editDep(self):
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
        for i in range(self.departments_table.rowCount()):
            id = self.departments_table.item(i, 0).text()
            name_dep = self.departments_table.item(i, 1).text()
            cursor.execute(
                "UPDATE department SET name_dep = '{}' WHERE department.id_dep = {};".format(
                    name_dep, id
                )
            )
            connection.commit()
        self.departments_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.edit_dep_table_ok.setVisible(False)
        connection.close()
        self.loadDep()
        self.loadDepCombo()

    # отслеживание события нажатия на отдел
    def itemClicked(self):
        self.del_department.setVisible(True)

    # удаление выбранного отдела из БД
    def delDep(self):
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
        row = self.departments_table.currentRow()
        id = self.departments_table.item(row, 0).text()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM department WHERE id_dep = {}".format(id))
        connection.commit()
        connection.close()
        self.loadDep()

    # скрытие кнопки для удаления
    def noDelDep(self):
        self.del_department.setVisible(False)

    # загрузка оклада всего отдела
    def loadSalaryDep(self):
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
        name_dep = self.comboBox_dep_2.currentText()
        cursor.execute(
            "select money from department where name_dep = '{}'".format(name_dep)
        )
        result = cursor.fetchall()
        if cursor.rowcount != 0:
            self.salary_dep.setText(str(result[0]["money"]))
        connection.close()

    # отслеживание изменения суммы отдела
    def EditSalaryDepStart(self):
        self.update_salary_dep.setVisible(True)

    def UpdateSalaryDep(self):
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
        money = self.salary_dep.text()
        name_dep = self.comboBox_dep_2.currentText()
        cursor.execute(
            "UPDATE `department` SET `money` = {} WHERE `department`.`name_dep` = '{}';".format(
                money, name_dep
            )
        )
        connection.commit()
        connection.close()
        self.loadSalaryDep()
        self.update_salary_dep.setVisible(False)

    # конец блока работы с отделами

    # работа с таблицей групп показателей:
    # загрузка групп в таблицу из БД
    def loadIndGroup(self):
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
        cursor.execute("SELECT * FROM `position_group` ")
        group_position = cursor.fetchall()
        self.ind_group_table.setRowCount(0)
        self.ind_group_table.setColumnCount(2)
        self.ind_group_table.hideColumn(0)
        self.ind_group_table.setHorizontalHeaderLabels(
            ["id", "Название группы показателей"]
        )
        for row_number, row_data in enumerate(group_position):
            self.ind_group_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.ind_group_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.ind_group_table.resizeColumnsToContents()
        connection.close()

    # открытие полей для создания новой группы
    def setAddIndGroupTrue(self):
        self.add_new_ind_group_ok.setVisible(True)
        self.ind_group_input_line.setVisible(True)
        self.add_new_ind_group_no.setVisible(True)
        self.ind_group_input_line.setText("")

    # закрытие полей для создания новой группы
    def setAddIndGroupFalse(self):
        self.add_new_ind_group_ok.setVisible(False)
        self.ind_group_input_line.setVisible(False)
        self.add_new_ind_group_no.setVisible(False)

    # добавление групп индикаторов в БД
    def addIndGroupToBD(self):
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
        name_ind_group = self.ind_group_input_line.text()
        cursor.execute(
            "INSERT INTO `position_group` (`id`, `name_group`) VALUES (NULL, '{}');".format(
                name_ind_group
            )
        )
        connection.commit()
        connection.close()
        self.loadIndGroup()
        self.setAddIndGroupFalse()

    # возможность редактировтаь поля в таблице, появление кнопки для завершения редактирования
    def setEditIndGroupTrue(self):
        self.ind_group_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
        )
        self.edit_ind_group_table_ok.setVisible(True)

    # обновление в БД всех измененных данных в таблице
    def editIndGroup(self):
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
        for i in range(self.ind_group_table.rowCount()):
            id = self.ind_group_table.item(i, 0).text()
            name_ind_group = self.ind_group_table.item(i, 1).text()
            cursor.execute(
                "UPDATE `position_group` SET `name_group` = '{}' WHERE `position_group`.`id` = {};".format(
                    name_ind_group, id
                )
            )
            connection.commit()
        self.ind_group_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.edit_ind_group_table_ok.setVisible(False)
        connection.close()
        self.loadIndGroup()

    # отслеживание события нажатия на группу индикаторов
    def itemClickedIndGroup(self):
        self.del_ind_group.setVisible(True)

    # удаление выбранной группы показателей из БД
    def delIndGroup(self):
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
        row = self.ind_group_table.currentRow()
        id = self.ind_group_table.item(row, 0).text()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM position_group WHERE id = {}".format(id))
        connection.commit()
        connection.close()
        self.loadIndGroup()

    # скрытие кнопки для удаления
    def noDelIndGroup(self):
        self.del_ind_group.setVisible(False)

    # закрытие блока групп показателей

    # блок окладов должностей
    def loadSalaryPos(self):
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
        name_dep = self.comboBox_dep_2.currentText()
        cursor.execute(
            "select name_pos, salary from position where department in (select id_dep from department where name_dep = '{}')".format(
                name_dep
            )
        )
        salary_pos = cursor.fetchall()
        self.salary_pos_table.setRowCount(0)
        self.salary_pos_table.setColumnCount(2)
        self.salary_pos_table.setHorizontalHeaderLabels(
            ["Название должности", "Должностной оклад"]
        )
        for row_number, row_data in enumerate(salary_pos):
            self.salary_pos_table.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.salary_pos_table.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.salary_pos_table.resizeColumnsToContents()
        connection.close()

    def editSalaryPosEdit(self):
        self.edit_salary_pos_table_ok.setVisible(True)
        self.salary_pos_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
        )

    def editSalaryPos(self):
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
        name_dep = self.comboBox_dep_2.currentText()
        for i in range(self.salary_pos_table.rowCount()):
            name_pos = self.salary_pos_table.item(i, 0).text()
            money = self.salary_pos_table.item(i, 1).text()
            cursor.execute(
                "UPDATE `position` SET `salary` = '{}' WHERE `position`.`name_pos` = '{}' AND department in (select id_dep from department where name_dep = '{}');".format(
                    money, name_pos, name_dep
                )
            )
            connection.commit()
            cursor.execute(
                "UPDATE fin_staff_salary SET salary_with_koaf_ind = {} * koaf * koaf_ind WHERE name_staff in (select id from staff where position in (select id from position where name_pos = '{}' and department in (select id_dep from department where name_dep = '{}')))".format(
                    money, name_pos, name_dep
                )
            )
            connection.commit()
        self.edit_salary_pos_table_ok.setVisible(False)
        self.salary_pos_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        connection.close()
        self.loadSalaryPos()

    # видимость кнопки для расчета ЗП для отедал бухов
    def countStaffForBuh(self):
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
        dep = self.comboBox_dep_2.currentText()
        cursor.execute(
            "SELECT COUNT(*) as count FROM `fin_staff_salary` where name_dep in (select department.id_dep from department where department.name_dep = '{}');".format(
                dep
            )
        )
        count = cursor.fetchall()
        fin = count[0]["count"]
        cursor.execute(
            "SELECT COUNT(*) as count FROM `staff` where position in (select id from position where department in (select department.id_dep from department where department.name_dep = '{}'));".format(
                dep
            )
        )
        count_s = cursor.fetchall()
        c_s = count_s[0]["count"]
        if fin == int(c_s):
            self.salary_dep_list.setVisible(True)
        else:
            self.salary_dep_list.setVisible(False)
        if int(c_s) == 0:
            self.salary_dep_list.setVisible(False)
        connection.close()

    # конец блока окладов должностей

    # блок ввода значения показателей в группы
    def loadGroupForEntered(self):
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
        name_dep = self.comboBox_dep.currentText()
        cursor.execute(
            "select DISTINCT position_group.name_group from position_group join pos_and_group on pos_and_group.id_group=position_group.id where id_pos in (select id from position where department in (select id_dep from department where name_dep = '{}'));".format(
                name_dep
            )
        )
        result = cursor.fetchall()
        self.ind_group_table_2.setRowCount(0)
        self.ind_group_table_2.setColumnCount(1)
        self.ind_group_table_2.setHorizontalHeaderLabels(
            ["Название группы показателей"]
        )
        for row_number, row_data in enumerate(result):
            self.ind_group_table_2.insertRow(row_number)
            for c_number, data in enumerate(row_data):
                self.ind_group_table_2.setItem(
                    row_number,
                    c_number,
                    QTableWidgetItem(str(row_data[data])),
                )
        self.ind_group_table_2.resizeColumnsToContents()
        connection.close()
        self.countStaffFinall()

    # видимость кнопки для расчета ЗП,а также отображение недостающих показателей
    def countStaffFinall(self):
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
        dep = self.comboBox_dep.currentText()
        cursor.execute(
            "SELECT COUNT(*) as count FROM `fin_staff_salary` where name_dep in (select department.id_dep from department where department.name_dep = '{}');".format(
                dep
            )
        )
        count = cursor.fetchall()
        fin = count[0]["count"]
        cursor.execute(
            "SELECT COUNT(*) as count FROM `staff` where position in (select id from position where department in (select department.id_dep from department where department.name_dep = '{}'));".format(
                dep
            )
        )
        count_s = cursor.fetchall()
        c_s = count_s[0]["count"]
        if fin == int(c_s):
            self.edit_salary_pos_table_true_2.setVisible(True)
        else:
            self.edit_salary_pos_table_true_2.setVisible(False)
        if int(c_s) == 0:
            self.edit_salary_pos_table_true_2.setVisible(False)
        for i in range(self.ind_group_table_2.rowCount()):
            name_group = self.ind_group_table_2.item(i, 0).text()
            cursor.execute(
                "SELECT COUNT(*) as count FROM `fin_staff_salary` where name_dep in (select department.id_dep from department where department.name_dep = '{}') and name_staff in (select id from staff where staff.position in (select id_pos from pos_and_group where id_group in (select position_group.id from position_group where position_group.name_group = '{}')))".format(
                    dep, name_group
                )
            )
            count = cursor.fetchall()
            ac_in_group_fin = count[0]["count"]
            cursor.execute(
                "SELECT COUNT(*) as count FROM `staff` where position in (select id from position where department in (select department.id_dep from department where department.name_dep = '{}')) and position in (select id_pos from pos_and_group where id_group in (select id from position_group where name_group = '{}'));".format(
                    dep, name_group
                )
            )
            count_s = cursor.fetchall()
            ac_in_group = count_s[0]["count"]
            self.ind_group_table_2.item(i, 0).setBackground(QtGui.QColor(255, 255, 255))
            if ac_in_group_fin != ac_in_group:
                self.ind_group_table_2.item(i, 0).setBackground(
                    QtGui.QColor(255, 255, 0)
                )
        connection.close()

    # очистить все показатели отдела
    def DelAllStaff(self):
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
        name_dep = self.comboBox_dep.currentText()
        countRow = self.ind_group_table_2.rowCount()
        for i in range(countRow):
            name_group = self.ind_group_table_2.item(i, 0).text()
            cursor.execute(
                "delete from indicators_values where name_ind in (select id from indicators where position_group in (select pos_and_group.id_group from pos_and_group where pos_and_group.id_group in (select position_group.id from position_group where name_group = '{}') and pos_and_group.id_pos in (select position.id from position where position.department in (select id_dep from department where name_dep = '{}')))) ".format(
                    name_group, name_dep
                )
            )
            connection.commit()
            cursor.execute(
                "delete from fin_staff_salary where name_dep in (select id_dep from department where name_dep = '{}')".format(
                    name_dep
                )
            )
            connection.commit()
        connection.close()
        self.countStaffFinall()

    # конец блока ввода показателей в группы

    # стартовые скрытые объекты
    def startHidden(self):
        self.dep_input_line.setVisible(False)
        self.ind_group_input_line.setVisible(False)
        self.add_new_dep_no.setVisible(False)
        self.add_new_dep_ok.setVisible(False)
        self.add_new_ind_group_no.setVisible(False)
        self.add_new_ind_group_ok.setVisible(False)
        self.edit_dep_table_ok.setVisible(False)
        self.edit_ind_group_table_ok.setVisible(False)
        self.edit_salary_pos_table_ok.setVisible(False)
        self.departments_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.del_department.setVisible(False)
        self.del_ind_group.setVisible(False)
        self.update_salary_dep.setVisible(False)
        self.salary_pos_table.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.edit_salary_pos_table_true_2.setVisible(False)
        self.salary_dep_list.setVisible(False)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1106, 885)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWindet = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWindet.setGeometry(QtCore.QRect(0, 0, 1111, 861))
        self.tabWindet.setObjectName("tabWindet")
        self.department = QtWidgets.QWidget()
        self.department.setObjectName("department")
        self.departments_table = QtWidgets.QTableWidget(parent=self.department)
        self.departments_table.setGeometry(QtCore.QRect(10, 180, 1081, 491))
        self.departments_table.setObjectName("departments_table")
        self.departments_table.setColumnCount(0)
        self.departments_table.setRowCount(0)
        self.create_new_dep = QtWidgets.QPushButton(parent=self.department)
        self.create_new_dep.setGeometry(QtCore.QRect(10, 70, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.create_new_dep.setFont(font)
        self.create_new_dep.setObjectName("create_new_dep")
        self.dep_input_line = QtWidgets.QLineEdit(parent=self.department)
        self.dep_input_line.setGeometry(QtCore.QRect(340, 70, 501, 41))
        self.dep_input_line.setObjectName("dep_input_line")
        self.add_new_dep_ok = QtWidgets.QPushButton(parent=self.department)
        self.add_new_dep_ok.setGeometry(QtCore.QRect(850, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_dep_ok.setFont(font)
        self.add_new_dep_ok.setObjectName("add_new_dep_ok")
        self.edit_dep_table_true = QtWidgets.QPushButton(parent=self.department)
        self.edit_dep_table_true.setGeometry(QtCore.QRect(10, 120, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_dep_table_true.setFont(font)
        self.edit_dep_table_true.setObjectName("edit_dep_table_true")
        self.edit_dep_table_ok = QtWidgets.QPushButton(parent=self.department)
        self.edit_dep_table_ok.setGeometry(QtCore.QRect(10, 690, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_dep_table_ok.setFont(font)
        self.edit_dep_table_ok.setObjectName("edit_dep_table_ok")
        self.add_new_dep_no = QtWidgets.QPushButton(parent=self.department)
        self.add_new_dep_no.setGeometry(QtCore.QRect(960, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_dep_no.setFont(font)
        self.add_new_dep_no.setObjectName("add_new_dep_no")
        self.department_list = QtWidgets.QLabel(parent=self.department)
        self.department_list.setGeometry(QtCore.QRect(360, 0, 351, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.department_list.setFont(font)
        self.department_list.setObjectName("department_list")
        self.del_department = QtWidgets.QPushButton(parent=self.department)
        self.del_department.setGeometry(QtCore.QRect(340, 120, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_department.setFont(font)
        self.del_department.setObjectName("del_department")
        self.tabWindet.addTab(self.department, "")
        self.ind_group = QtWidgets.QWidget()
        self.ind_group.setObjectName("ind_group")
        self.ind_group_list = QtWidgets.QLabel(parent=self.ind_group)
        self.ind_group_list.setGeometry(QtCore.QRect(340, 0, 401, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ind_group_list.setFont(font)
        self.ind_group_list.setObjectName("ind_group_list")
        self.create_new_ind_group = QtWidgets.QPushButton(parent=self.ind_group)
        self.create_new_ind_group.setGeometry(QtCore.QRect(10, 70, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.create_new_ind_group.setFont(font)
        self.create_new_ind_group.setObjectName("create_new_ind_group")
        self.ind_group_input_line = QtWidgets.QLineEdit(parent=self.ind_group)
        self.ind_group_input_line.setGeometry(QtCore.QRect(340, 70, 501, 41))
        self.ind_group_input_line.setObjectName("ind_group_input_line")
        self.add_new_ind_group_ok = QtWidgets.QPushButton(parent=self.ind_group)
        self.add_new_ind_group_ok.setGeometry(QtCore.QRect(850, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_ind_group_ok.setFont(font)
        self.add_new_ind_group_ok.setObjectName("add_new_ind_group_ok")
        self.add_new_ind_group_no = QtWidgets.QPushButton(parent=self.ind_group)
        self.add_new_ind_group_no.setGeometry(QtCore.QRect(960, 70, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_new_ind_group_no.setFont(font)
        self.add_new_ind_group_no.setObjectName("add_new_ind_group_no")
        self.edit_ind_group_table_true = QtWidgets.QPushButton(parent=self.ind_group)
        self.edit_ind_group_table_true.setGeometry(QtCore.QRect(10, 120, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_ind_group_table_true.setFont(font)
        self.edit_ind_group_table_true.setObjectName("edit_ind_group_table_true")
        self.del_ind_group = QtWidgets.QPushButton(parent=self.ind_group)
        self.del_ind_group.setGeometry(QtCore.QRect(340, 120, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_ind_group.setFont(font)
        self.del_ind_group.setObjectName("del_ind_group")
        self.ind_group_table = QtWidgets.QTableWidget(parent=self.ind_group)
        self.ind_group_table.setGeometry(QtCore.QRect(10, 180, 1081, 491))
        self.ind_group_table.setObjectName("ind_group_table")
        self.ind_group_table.setColumnCount(0)
        self.ind_group_table.setRowCount(0)
        self.edit_ind_group_table_ok = QtWidgets.QPushButton(parent=self.ind_group)
        self.edit_ind_group_table_ok.setGeometry(QtCore.QRect(10, 690, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_ind_group_table_ok.setFont(font)
        self.edit_ind_group_table_ok.setObjectName("edit_ind_group_table_ok")
        self.tabWindet.addTab(self.ind_group, "")
        self.salary_pos = QtWidgets.QWidget()
        self.salary_pos.setObjectName("salary_pos")
        self.label_2 = QtWidgets.QLabel(parent=self.salary_pos)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.comboBox_dep_2 = QtWidgets.QComboBox(parent=self.salary_pos)
        self.comboBox_dep_2.setGeometry(QtCore.QRect(160, 50, 391, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_dep_2.setFont(font)
        self.comboBox_dep_2.setObjectName("comboBox_dep_2")
        self.salary_dep = QtWidgets.QLineEdit(parent=self.salary_pos)
        self.salary_dep.setGeometry(QtCore.QRect(600, 50, 201, 41))
        self.salary_dep.setObjectName("salary_dep")
        self.update_salary_dep = QtWidgets.QPushButton(parent=self.salary_pos)
        self.update_salary_dep.setGeometry(QtCore.QRect(830, 50, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.update_salary_dep.setFont(font)
        self.update_salary_dep.setObjectName("update_salary_dep")
        self.salary_pos_table = QtWidgets.QTableWidget(parent=self.salary_pos)
        self.salary_pos_table.setGeometry(QtCore.QRect(10, 180, 1081, 491))
        self.salary_pos_table.setObjectName("salary_pos_table")
        self.salary_pos_table.setColumnCount(0)
        self.salary_pos_table.setRowCount(0)
        self.edit_salary_pos_table_true = QtWidgets.QPushButton(parent=self.salary_pos)
        self.edit_salary_pos_table_true.setGeometry(QtCore.QRect(10, 120, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_salary_pos_table_true.setFont(font)
        self.edit_salary_pos_table_true.setObjectName("edit_salary_pos_table_true")
        self.salary_dep_list = QtWidgets.QPushButton(parent=self.salary_pos)
        self.salary_dep_list.setGeometry(QtCore.QRect(830, 50, 255, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.salary_dep_list.setFont(font)
        self.salary_dep_list.setObjectName("edit_salary_pos_table_true")
        self.edit_salary_pos_table_ok = QtWidgets.QPushButton(parent=self.salary_pos)
        self.edit_salary_pos_table_ok.setGeometry(QtCore.QRect(10, 680, 321, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_salary_pos_table_ok.setFont(font)
        self.edit_salary_pos_table_ok.setObjectName("edit_salary_pos_table_ok")
        self.tabWindet.addTab(self.salary_pos, "")
        self.set_value = QtWidgets.QWidget()
        self.set_value.setObjectName("set_value")
        self.label = QtWidgets.QLabel(parent=self.set_value)
        self.label.setGeometry(QtCore.QRect(30, 90, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.comboBox_dep = QtWidgets.QComboBox(parent=self.set_value)
        self.comboBox_dep.setGeometry(QtCore.QRect(160, 90, 391, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox_dep.setFont(font)
        self.comboBox_dep.setObjectName("comboBox_dep")
        self.del_all = QtWidgets.QPushButton(parent=self.set_value)
        self.del_all.setGeometry(QtCore.QRect(10, 680, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_all.setFont(font)
        self.del_all.setObjectName("del_all")
        self.ind_group_table_2 = QtWidgets.QTableWidget(parent=self.set_value)
        self.ind_group_table_2.setGeometry(QtCore.QRect(10, 180, 1081, 491))
        self.ind_group_table_2.setObjectName("ind_group_table_2")
        self.ind_group_table_2.setColumnCount(0)
        self.ind_group_table_2.setRowCount(0)
        self.ind_group_list_2 = QtWidgets.QLabel(parent=self.set_value)
        self.ind_group_list_2.setGeometry(QtCore.QRect(300, 0, 461, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.ind_group_list_2.setFont(font)
        self.ind_group_list_2.setObjectName("ind_group_list_2")
        self.edit_salary_pos_table_true_2 = QtWidgets.QPushButton(parent=self.set_value)
        self.edit_salary_pos_table_true_2.setGeometry(QtCore.QRect(590, 90, 501, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_salary_pos_table_true_2.setFont(font)
        self.edit_salary_pos_table_true_2.setObjectName("edit_salary_pos_table_true_2")
        self.tabWindet.addTab(self.set_value, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWindet.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.add_new_dep_ok.clicked.connect(self.addDepToBD)
        self.add_new_dep_ok.clicked.connect(self.loadDepCombo)
        self.create_new_dep.clicked.connect(self.setAddDeptTrue)
        self.add_new_dep_no.clicked.connect(self.setAddDeptFalse)
        self.del_department.clicked.connect(self.delDep)
        self.del_department.clicked.connect(self.loadDepCombo)
        self.edit_dep_table_true.clicked.connect(self.setEditDepTrue)
        self.edit_dep_table_ok.clicked.connect(self.editDep)
        self.departments_table.itemClicked.connect(self.itemClicked)
        self.departments_table.itemDoubleClicked.connect(self.staff_and_pos_widget)
        self.create_new_ind_group.clicked.connect(self.setAddIndGroupTrue)
        self.add_new_ind_group_ok.clicked.connect(self.addIndGroupToBD)
        self.add_new_ind_group_ok.clicked.connect(self.loadGroupForEntered)
        self.add_new_ind_group_no.clicked.connect(self.setAddIndGroupFalse)
        self.edit_ind_group_table_true.clicked.connect(self.setEditIndGroupTrue)
        self.edit_ind_group_table_ok.clicked.connect(self.editIndGroup)
        self.ind_group_table.itemClicked.connect(self.itemClickedIndGroup)
        self.del_ind_group.clicked.connect(self.delIndGroup)
        self.tabWindet.currentChanged.connect(self.loadGroupForEntered)
        self.tabWindet.currentChanged.connect(self.loadIndGroup)
        self.tabWindet.currentChanged.connect(self.startHidden)
        self.tabWindet.currentChanged.connect(self.countStaffFinall)
        self.tabWindet.currentChanged.connect(self.loadSalaryPos)
        self.comboBox_dep.currentIndexChanged.connect(self.loadGroupForEntered)
        self.comboBox_dep.currentIndexChanged.connect(self.countStaffFinall)
        self.ind_group_table.itemDoubleClicked.connect(self.indicators_widget)
        self.ind_group_table_2.itemDoubleClicked.connect(self.finally_salary_widget)
        self.salary_dep.textEdited.connect(self.EditSalaryDepStart)
        self.update_salary_dep.clicked.connect(self.UpdateSalaryDep)
        self.comboBox_dep_2.currentIndexChanged.connect(self.loadSalaryDep)
        self.comboBox_dep_2.currentIndexChanged.connect(self.loadSalaryPos)
        self.edit_salary_pos_table_true.clicked.connect(self.editSalaryPosEdit)
        self.edit_salary_pos_table_ok.clicked.connect(self.editSalaryPos)
        self.edit_salary_pos_table_true_2.clicked.connect(self.fin_salary_dep_widget)
        self.del_all.clicked.connect(self.DelAllStaff)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Эффективный контракт"))
        self.create_new_dep.setText(_translate("MainWindow", "Создать подразделение"))
        self.add_new_dep_ok.setText(_translate("MainWindow", "OK"))
        self.edit_dep_table_true.setText(_translate("MainWindow", "Редактировать"))
        self.edit_dep_table_ok.setText(_translate("MainWindow", "Готово"))
        self.add_new_dep_no.setText(_translate("MainWindow", "Отмена"))
        self.department_list.setText(_translate("MainWindow", "Список подразделений"))
        self.del_department.setText(_translate("MainWindow", "Удалить подразделение"))
        self.tabWindet.setTabText(
            self.tabWindet.indexOf(self.department),
            _translate("MainWindow", "Подразделения"),
        )
        self.ind_group_list.setText(
            _translate("MainWindow", "Список групп показателей")
        )
        self.create_new_ind_group.setText(
            _translate("MainWindow", "Создать группу показателей")
        )
        self.add_new_ind_group_ok.setText(_translate("MainWindow", "OK"))
        self.add_new_ind_group_no.setText(_translate("MainWindow", "Отмена"))
        self.edit_ind_group_table_true.setText(
            _translate("MainWindow", "Редактировать")
        )
        self.del_ind_group.setText(_translate("MainWindow", "Удалить группу"))
        self.edit_ind_group_table_ok.setText(_translate("MainWindow", "Готово"))
        self.tabWindet.setTabText(
            self.tabWindet.indexOf(self.ind_group),
            _translate("MainWindow", "Группы показателей"),
        )
        self.label_2.setText(_translate("MainWindow", "Отдел"))
        self.update_salary_dep.setText(_translate("MainWindow", "Изменить сумму"))
        self.edit_salary_pos_table_true.setText(
            _translate("MainWindow", "Редактировать")
        )
        self.edit_salary_pos_table_ok.setText(_translate("MainWindow", "Готово"))
        self.tabWindet.setTabText(
            self.tabWindet.indexOf(self.salary_pos), _translate("MainWindow", "Оклады")
        )
        self.label.setText(_translate("MainWindow", "Отдел"))
        self.ind_group_list_2.setText(
            _translate("MainWindow", "Заполнить показатели отдела")
        )
        self.edit_salary_pos_table_true_2.setText(
            _translate("MainWindow", "Рассчитать заработную плату отдела")
        )
        self.del_all.setText(_translate("MainWindow", "Очистить"))
        self.tabWindet.setTabText(
            self.tabWindet.indexOf(self.set_value),
            _translate("MainWindow", "Заполнить показатели"),
        )
        self.salary_dep_list.setText(
            _translate("MainWindow", "Посмотреть отчет по отделу")
        )
        self.loadDep()
        self.loadDepCombo()
        self.loadIndGroup()
        self.startHidden()
        self.loadSalaryDep()
        self.loadSalaryPos()
        self.loadGroupForEntered()
        self.countStaffFinall()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
