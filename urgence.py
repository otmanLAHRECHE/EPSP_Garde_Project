from PyQt5 import uic, QtWidgets, QtSql
from PyQt5.QtWidgets import *
import sys


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)

        self.con = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("/home/contacts.sqlite")

        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes de garde")
        self.tab.setTabText(1, "Medecins")

        self.tab_gardes = self.findChild(QWidget, "tab")
        self.tab_medcines = self.findChild(QWidget, "tab_2")
        self.tablelayout = self.findChild(QWidget, "widget_2")
        self.medcinname = self.findChild(QLineEdit, "lineEdit")

        self.add = self.findChild(QPushButton, "pushButton")
        self.update = self.findChild(QPushButton, "pushButton_3")
        self.delete = self.findChild(QPushButton, "pushButton_2")









