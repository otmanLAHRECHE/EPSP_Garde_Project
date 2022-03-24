import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTableWidget, QMessageBox

basedir = os.path.dirname(__file__)


class UrgenceInfUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceInfUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'urgence_inf.ui'), self)

        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes de garde")
        self.tab.setTabText(1, "Infirmiers survients")
        self.tab.setTabText(2, "Infirmiers")
        self.medcinname = self.findChild(QLineEdit, "lineEdit")
        self.add_garde = self.findChild(QPushButton, "pushButton_4")
        self.add_garde.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))

        self.add = self.findChild(QPushButton, "pushButton")
        self.add.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))
        self.update = self.findChild(QPushButton, "pushButton_3")
        self.update.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'edit.png')))
        self.delete = self.findChild(QPushButton, "pushButton_2")
        self.delete.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'user-x.png')))
        self.table = self.findChild(QTableWidget, "tableWidget")
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 110)

        self.table_group = self.findChild(QTableWidget, "tableWidget_3")
        self.table_group.setColumnWidth(0, 80)
        self.table_group.setColumnWidth(1, 200)
        self.table_group.setColumnWidth(2, 110)
        self.table_group.setColumnWidth(3, 110)

        self.add_group = self.findChild(QPushButton, "pushButton_7")
        self.add_group.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))
        self.update_group = self.findChild(QPushButton, "pushButton_6")
        self.update_group.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'edit.png')))
        self.delete_group = self.findChild(QPushButton, "pushButton_5")
        self.delete_group.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'user-x.png')))



        self.table_gardes = self.findChild(QTableWidget, "tableWidget_2")


        self.table_gardes.setColumnWidth(0, 150)
        self.table_gardes.setColumnWidth(1, 150)
        self.table_gardes.setColumnWidth(2, 150)
        self.table_gardes.setColumnWidth(3, 180)
        self.table_gardes.setColumnWidth(4, 270)
        self.table_gardes.hideColumn(0)

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



