import sqlite3

from PyQt5 import uic, QtWidgets, QtSql, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)

        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes de garde")
        self.tab.setTabText(1, "Medecins")

        self.tab_gardes = self.findChild(QWidget, "tab")
        self.tab_medcines = self.findChild(QWidget, "tab_2")
        self.tablelayout = self.findChild(QWidget, "widget_2")
        self.medcinname = self.findChild(QLineEdit, "lineEdit")

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
        self.loadUsers()

        self.add.clicked.connect(self.add_toDb)

    def alert_no_name(self):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText('Le champ de nom est vide!')
        alert.exec_()

    def add_toDb(self):
        if self.medcinname.text() == "":
            self.alert_no_name()
        else:
            connection = sqlite3.connect('database/sqlite.db')
            print("connection")
            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.medcinname.text(), 'medecin urgence')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.loadUsers()

    def loadUsers(self):
        print("load users")
        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()
        sql_q = 'SELECT * FROM health_worker where service=?'
        tablerow = 0
        cur.execute(sql_q, ('medecin urgence',))
        results = cur.fetchall()
        for row in results:
            print(row)
            self.table.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.table.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.table.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow += 1
        connection.close()
