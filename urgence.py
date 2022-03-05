from PyQt5 import uic, QtWidgets, QtSql, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)

        self.con = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.con.setDatabaseName("database/sqlite.db")

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

        self.model = QtSql.QSqlTableModel()
        self.model.setTable('health_worker')
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Nom et Prenom")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Service")

        self.table = self.findChild(QTableView, "tableView")

        self.table.setModel(self.model)
        self.i = self.model.rowCount()

        self.add.clicked.connect(self.add_toDb())
        self.update.clicked.connect(self.update_toDb())
        self.delete.clicked.connect(self.delete_toDb())

    def alert_no_name(self):
        alert = QMessageBox()
        alert.setText('Le champ de nom est vide!')
        alert.exec_()

    def add_toDb(self):
        print(self.i)
        if self.medcinname.text() == "":
            self.alert_no_name()
        else:
            self.model.insertRows(self.i, 1)
            self.model.setData(self.model.index(self.i, 1), self.ui.lineEdit.text())
            self.model.setData(self.model.index(self.i, 2), self.ui.lineEdit_2.text())
            self.model.submitAll()
            self.i += 1

    def delete_toDb(self):
        if self.table.currentIndex().row() > -1:
            self.model.removeRow(self.table.currentIndex().row())
            self.i -= 1
            self.model.select()

    def update_toDb(self):
        if self.table.currentIndex().row() > -1:
            record = self.model.record(self.ui.tableWidget.currentIndex().row())
            record.setValue("Name", self.ui.lineEdit.text())
            record.setValue("Surname", self.ui.lineEdit_2.text())
            record.setValue("DOB", self.ui.dateEdit.text())
            record.setValue("Phone", self.ui.lineEdit_3.text())
            self.model.setRecord(self.ui.tableWidget.currentIndex().row(), record)
