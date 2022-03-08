import datetime
import sqlite3

from PyQt5 import QtWidgets, uic
from calendar import monthrange

from PyQt5.QtWidgets import QTableWidgetItem

from widgets import Chose_worker


class UrgenceGuardUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(UrgenceGuardUi, self).__init__()
        uic.loadUi('ui/guard_urgence.ui', self)

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 220)

        self.month = month
        self.year = year
        self.num_days = monthrange(self.year, self.month)[1]
        self.num_days = self.num_days - 1
        print(self.num_days)

        if self.month == 1:
            m = "janvier"
        elif self.month == 2:
            m = "février"
        elif self.month == 3:
            m = "mars"
        elif self.month == 4:
            m = "avril"
        elif self.month == 5:
            m = "mai"
        elif self.month == 6:
            m = "juin"
        elif self.month == 7:
            m = "juillet"
        elif self.month == 8:
            m = "août"
        elif self.month == 9:
            m = "septembre"
        elif self.month == 10:
            m = "octobre"
        elif self.month == 11:
            m = "novembre"
        elif self.month == 12:
            m = "décembre"

        self.ttl.setText("Planing de garde urgence mois " + str(m) + "/" + str(self.year) + ":")
        self.load_med()
        self.load_guards()

        print(self.medcins)

    def load_guards(self):
        print("load guard list")

        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()


        for row in range(self.num_days):
            print(row)
            day = row + 1
            x = datetime.datetime(self.year, self.month, day)
            m = ""
            if x.strftime("%A") == "Saturday":
                m = "Samedi"
            elif x.strftime("%A") == "Sunday":
                m = "Dimanche"
            elif x.strftime("%A") == "Monday":
                m = "Lundi"
            elif x.strftime("%A") == "Tuesday":
                m = "Mardi"
            elif x.strftime("%A") == "Wednesday":
                m = "Mercredi"
            elif x.strftime("%A") == "Thursday":
                m = "Jeudi"
            elif x.strftime("%A") == "Friday":
                m = "Vendredi"

            sql_q = 'SELECT full_name FROM guard where service=?'
            tablerow = 0
            cur.execute(sql_q, ('urgence',))
            results = cur.fetchall()

            self.table.setRowHeight(row, 50)
            self.table.setItem(row, 0, QTableWidgetItem(m))
            self.table.setItem(row, 1, QTableWidgetItem(str(day) + "/" + str(self.month) + "/" + str(self.year)))
            chose_light = Chose_worker()
            chose_night = Chose_worker()
            self.table.setCellWidget(row, 2, chose_light)
            self.table.setCellWidget(row, 3, chose_night)
            """
            self.table_gardes.setItem(row, 2, QTableWidgetItem(str(row[2])))
            self.table_gardes.setItem(row, 3, QTableWidgetItem(row[3]))
            buttons = Buttons()
            self.table_gardes.setCellWidget(tablerow, 4, buttons)
            """
    def load_med(self):
        print("load medecins")
        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()
        sql_q = 'SELECT full_name FROM health_worker where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence',))
        self.medcins = cur.fetchall()
        connection.close()
