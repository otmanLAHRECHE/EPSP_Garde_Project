import sqlite3

from PyQt5 import uic, QtWidgets, QtSql, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys

from dialogs import Update_worker_dialog, Add_new_month
from widgets import Buttons


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)

        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes de garde")
        self.tab.setTabText(1, "Medecins")

        self.tab_gardes = self.findChild(QWidget, "tab")
        self.tab_medcines = self.findChild(QWidget, "tab_2")
        self.medcinname = self.findChild(QLineEdit, "lineEdit")
        self.add_garde = self.findChild(QPushButton, "pushButton_4")
        self.add_garde.setIcon(QIcon("asstes/images/plus.png"))

        self.add = self.findChild(QPushButton, "pushButton")
        self.add.setIcon(QIcon("asstes/images/plus.png"))
        self.update = self.findChild(QPushButton, "pushButton_3")
        self.update.setIcon(QIcon("asstes/images/edit.png"))
        self.delete = self.findChild(QPushButton, "pushButton_2")
        self.delete.setIcon(QIcon("asstes/images/user-x.png"))
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 110)

        self.table_gardes = self.findChild(QTableWidget, "tableWidget_2")

        self.table_gardes.setColumnWidth(0, 150)
        self.table_gardes.setColumnWidth(1, 150)
        self.table_gardes.setColumnWidth(2, 180)
        self.table_gardes.setColumnWidth(3, 220)

        self.loadGuardMonths()
        self.loadUsers()

        self.add.clicked.connect(self.add_toDb)
        self.delete.clicked.connect(self.deleteUser)
        self.update.clicked.connect(self.updateUser)
        self.add_garde.clicked.connect(self.add_grd)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def add_toDb(self):
        if self.medcinname.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)
        else:
            connection = sqlite3.connect('database/sqlite.db')
            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.medcinname.text(), 'urgence')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.medcinname.setText("")
            self.loadUsers()

    def add_grd(self):
        dialog = Add_new_month()
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.year.text() == "":
                message = "Entrer une valid année"
                self.alert_(message)
            else:
                connection = sqlite3.connect('database/sqlite.db')
                cur = connection.cursor()
                sql_q = "INSERT INTO guard_mounth (m,y,service) values (?,?,?)"
                m = 0
                if dialog.month.currentIndex() == 0:
                    m = 1
                elif dialog.month.currentIndex() == 1:
                    m = 2
                elif dialog.month.currentIndex() == 2:
                    m = 3
                elif dialog.month.currentIndex() == 3:
                    m = 4
                elif dialog.month.currentIndex() == 4:
                    m = 5
                elif dialog.month.currentIndex() == 5:
                    m = 6
                elif dialog.month.currentIndex() == 6:
                    m = 7
                elif dialog.month.currentIndex() == 7:
                    m = 8
                elif dialog.month.currentIndex() == 8:
                    m = 9
                elif dialog.month.currentIndex() == 9:
                    m = 10
                elif dialog.month.currentIndex() == 10:
                    m = 11
                elif dialog.month.currentIndex() == 11:
                    m = 12

                guard_m = (m, int(dialog.year.text()), 'urgence')
                print(guard_m)

                cur.execute(sql_q, guard_m)
                connection.commit()
                connection.close()
                self.loadGuardMonths()

    def deleteUser(self):
        row = self.table.currentRow()
        print(row)
        if row > -1:
            id = self.table.item(row, 0).text()
            connection = sqlite3.connect('database/sqlite.db')
            cur = connection.cursor()
            sql_q = 'DELETE FROM health_worker WHERE worker_id=?'
            cur.execute(sql_q, (id,))
            connection.commit()
            connection.close()
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.loadUsers()
        else:
            message = 'Selectioner un medecin'
            self.alert_(message)

    def updateUser(self):
        row = self.table.currentRow()
        print(row)
        if row > -1:
            dialog = Update_worker_dialog()
            print("dialog")
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.worker.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                else:
                    id = self.table.item(row, 0).text()
                    connection = sqlite3.connect('database/sqlite.db')
                    cur = connection.cursor()
                    sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
                    cur.execute(sql_q, (dialog.worker.text(), id))
                    connection.commit()
                    connection.close()
                    self.loadUsers()

        else:
            message = 'Selectioner un medecin'
            self.alert_(message)

    def loadUsers(self):
        print("load users")
        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()
        sql_q = 'SELECT * FROM health_worker where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence',))
        results = cur.fetchall()
        for row in results:
            print(row)
            self.table.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.table.setItem(tablerow, 2, QTableWidgetItem(row[2]))
            tablerow += 1
        self.table.setItem(tablerow, 0, QTableWidgetItem(""))
        self.table.setItem(tablerow, 1, QTableWidgetItem(""))
        self.table.setItem(tablerow, 2, QTableWidgetItem(""))
        connection.close()

    def loadGuardMonths(self):
        print("load guards")
        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()
        sql_q = 'SELECT * FROM guard_mounth where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence',))
        results = cur.fetchall()
        for row in results:
            print(row)
            self.table_gardes.setRowHeight(tablerow, 70)
            m = ""
            if row[1] == 1:
                m = "janvier"
            elif row[1] == 2:
                m = "février"
            elif row[1] == 3:
                m = "mars"
            elif row[1] == 4:
                m = "avril"
            elif row[1] == 5:
                m = "mai"
            elif row[1] == 6:
                m = "juin"
            elif row[1] == 7:
                m = "juillet"
            elif row[1] == 8:
                m = "août"
            elif row[1] == 9:
                m = "septembre"
            elif row[1] == 10:
                m = "octobre"
            elif row[1] == 11:
                m = "novembre"
            elif row[1] == 12:
                m = "décembre"

            self.table_gardes.setItem(tablerow, 0, QTableWidgetItem(m))
            self.table_gardes.setItem(tablerow, 1, QTableWidgetItem(str(row[2])))
            self.table_gardes.setItem(tablerow, 2, QTableWidgetItem(row[3]))
            buttons = Buttons()
            self.table_gardes.setCellWidget(tablerow, 3, buttons)
            buttons.print_garde.clicked.connect(self.print_g)
            buttons.edit_garde.clicked.connect(self.edit_g)
            buttons.delete_garde.clicked.connect(self.delete_g)

            tablerow += 1
        connection.close()

    def edit_g(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        print(index.row())

    def delete_g(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        print(index.row())

    def print_g(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        print(index.row())
