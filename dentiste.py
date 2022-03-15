import os
import sqlite3

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QTableWidget, QMessageBox, QTableWidgetItem, qApp

from dentiste_consultation import DentisteConsultationUi
from dentiste_guard import DentisteGuardUi
from dialogs import Add_new_month, Update_worker_dialog
import export_dentiste_consultation
import export_dentiste_guard
from tools import get_workers_count, get_guard_months_count, get_consultation_months_count

from widgets import Buttons
basedir = os.path.dirname(__file__)


class DentisteMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DentisteMainUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'dentiste.ui'), self)


        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab.setTabText(0, "Listes des gardes")
        self.tab.setTabText(1, "Liste des consultations")
        self.tab.setTabText(2, "Liste des dentistes")

        self.dentistename = self.findChild(QLineEdit, "lineEdit")
        self.add_garde = self.findChild(QPushButton, "pushButton_4")
        self.add_garde.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))


        self.add_consultation = self.findChild(QPushButton, "pushButton_5")
        self.add_consultation.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))

        self.add_consultation = self.findChild(QPushButton, "pushButton_5")
        self.add_consultation.setIcon(QIcon(os.path.join(basedir, 'asstes', 'images', 'plus.png')))

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

        self.table_gardes = self.findChild(QTableWidget, "tableWidget_2")

        self.table_gardes.setColumnWidth(0, 150)
        self.table_gardes.setColumnWidth(1, 150)
        self.table_gardes.setColumnWidth(2, 150)
        self.table_gardes.setColumnWidth(3, 180)
        self.table_gardes.setColumnWidth(4, 220)
        self.table_gardes.hideColumn(0)

        self.table_consultation = self.findChild(QTableWidget, "tableWidget_3")

        self.table_consultation.setColumnWidth(0, 150)
        self.table_consultation.setColumnWidth(1, 150)
        self.table_consultation.setColumnWidth(2, 150)
        self.table_consultation.setColumnWidth(3, 180)
        self.table_consultation.setColumnWidth(4, 220)
        self.table_consultation.hideColumn(0)

        self.loadGuardMonths()
        self.loadConsultationMonths()
        self.loadUsers()

        self.add.clicked.connect(self.add_toDb)
        self.delete.clicked.connect(self.deleteUser)
        self.update.clicked.connect(self.updateUser)
        self.add_garde.clicked.connect(self.add_grd)
        self.add_consultation.clicked.connect(self.add_cns)

    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def add_toDb(self):
        med_count = get_workers_count("dentiste")[0]
        if self.dentistename.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)

        elif med_count[0] > 25:
            message = 'Maximum nombre des dentistes, supremer un dentiste'
            self.alert_(message)
        else:
            connection = sqlite3.connect("database/sqlite.db")

            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.dentistename.text(), 'dentiste')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.dentistename.setText("")
            self.loadUsers()

    def add_grd(self):

        guards_months_count = get_guard_months_count("dentiste")[0]

        dialog = Add_new_month()
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.year.text() == "":
                message = "Entrer une valid année"
                self.alert_(message)
            elif guards_months_count[0] > 13:
                message = "Maximum liste des garde, suprimrer des listes"
                self.alert_(message)
            else:
                connection = sqlite3.connect("database/sqlite.db")
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

                guard_m = (m, int(dialog.year.text()), 'dentiste')
                print(guard_m)

                cur.execute(sql_q, guard_m)
                connection.commit()
                connection.close()
                self.loadGuardMonths()

    def deleteUser(self):
        row = self.table.currentRow()
        if row > -1:
            id = self.table.item(row, 0).text()
            connection = sqlite3.connect("database/sqlite.db")
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
            message = 'Selectioner un dentiste'
            self.alert_(message)

    def updateUser(self):
        row = self.table.currentRow()
        if row > -1:
            dialog = Update_worker_dialog()
            print("dialog")
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.worker.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                else:
                    id = self.table.item(row, 0).text()
                    connection = sqlite3.connect("database/sqlite.db")
                    cur = connection.cursor()
                    sql_q = 'UPDATE health_worker SET full_name= ? WHERE worker_id= ?'
                    cur.execute(sql_q, (dialog.worker.text(), id))
                    connection.commit()
                    connection.close()
                    self.loadUsers()

        else:
            message = 'Selectioner un dentiste'
            self.alert_(message)

    def loadUsers(self):
        print("load users")
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT * FROM health_worker where service=?'
        tablerow = 0
        cur.execute(sql_q, ('dentiste',))
        results = cur.fetchall()
        for row in results:
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
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT * FROM guard_mounth where service=?'
        tablerow = 0
        cur.execute(sql_q, ('dentiste',))
        results = cur.fetchall()
        for row in results:
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

            self.table_gardes.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.table_gardes.setItem(tablerow, 1, QTableWidgetItem(m))
            self.table_gardes.setItem(tablerow, 2, QTableWidgetItem(str(row[2])))
            self.table_gardes.setItem(tablerow, 3, QTableWidgetItem(row[3]))
            buttons = Buttons()
            self.table_gardes.setCellWidget(tablerow, 4, buttons)
            buttons.print_garde.clicked.connect(self.print_g)
            buttons.edit_garde.clicked.connect(self.edit_g)
            buttons.delete_garde.clicked.connect(self.delete_g)

            tablerow += 1
        self.table_gardes.setItem(tablerow, 0, QTableWidgetItem(""))
        self.table_gardes.setItem(tablerow, 1, QTableWidgetItem(""))
        self.table_gardes.setItem(tablerow, 2, QTableWidgetItem(""))
        self.table_gardes.setItem(tablerow, 3, QTableWidgetItem(""))
        self.table_gardes.removeCellWidget(tablerow, 4)
        connection.close()

    def edit_g(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        row = index.row()
        m = self.table_gardes.item(row, 1).text()
        y = self.table_gardes.item(row, 2).text()
        if m == "janvier":
            m = 1
        elif m == "février":
            m = 2
        elif m == "mars":
            m = 3
        elif m == "avril":
            m = 4
        elif m == "mai":
            m = 5
        elif m == "juin":
            m = 6
        elif m == "juillet":
            m = 7
        elif m == "août":
            m = 8
        elif m == "septembre":
            m = 9
        elif m == "octobre":
            m = 10
        elif m == "novembre":
            m = 11
        elif m == "décembre":
            m = 12

        y = int(y)

        self.dentiste_guard_page = DentisteGuardUi(m, y)
        self.dentiste_guard_page.show()
        self.close()

    def delete_g(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        row = index.row()
        if row > -1:
            id = self.table_gardes.item(row, 0).text()
            connection = sqlite3.connect("database/sqlite.db")
            cur = connection.cursor()
            sql_q = 'DELETE FROM guard_mounth WHERE guard_mounth_id=?'
            cur.execute(sql_q, (id,))
            connection.commit()
            connection.close()
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.table.setItem(row, 3, QTableWidgetItem(""))
            self.table.setItem(row, 4, QTableWidgetItem(""))
            self.loadGuardMonths()

    def print_g(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        row = index.row()
        m = self.table_gardes.item(row, 1).text()
        y = self.table_gardes.item(row, 2).text()
        if m == "janvier":
            m = 1
        elif m == "février":
            m = 2
        elif m == "mars":
            m = 3
        elif m == "avril":
            m = 4
        elif m == "mai":
            m = 5
        elif m == "juin":
            m = 6
        elif m == "juillet":
            m = 7
        elif m == "août":
            m = 8
        elif m == "septembre":
            m = 9
        elif m == "octobre":
            m = 10
        elif m == "novembre":
            m = 11
        elif m == "décembre":
            m = 12

        y = int(y)

        self.next_page = export_dentiste_guard.ExportDentisteGuardUi(m, y)
        self.close()
        self.next_page.show()

    def add_cns(self):

        consultations_months_count = get_consultation_months_count("dentiste")[0]

        dialog = Add_new_month()
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.year.text() == "":
                message = "Entrer une valid année"
                self.alert_(message)
            elif consultations_months_count[0] > 13:
                message = "Maximum liste des consultations, suprimrer des listes"
                self.alert_(message)
            else:
                connection = sqlite3.connect("database/sqlite.db")
                cur = connection.cursor()
                sql_q = "INSERT INTO consultaion_mounth (m,y,service) values (?,?,?)"
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

                consultation_m = (m, int(dialog.year.text()), 'dentiste')

                cur.execute(sql_q, consultation_m)
                connection.commit()
                connection.close()
                self.loadConsultationMonths()

    def loadConsultationMonths(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT * FROM consultaion_mounth where service=?'
        tablerow = 0
        cur.execute(sql_q, ('dentiste',))
        results = cur.fetchall()
        for row in results:
            self.table_consultation.setRowHeight(tablerow, 70)
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

            self.table_consultation.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.table_consultation.setItem(tablerow, 1, QTableWidgetItem(m))
            self.table_consultation.setItem(tablerow, 2, QTableWidgetItem(str(row[2])))
            self.table_consultation.setItem(tablerow, 3, QTableWidgetItem(row[3]))
            buttons = Buttons()
            self.table_consultation.setCellWidget(tablerow, 4, buttons)
            buttons.print_garde.clicked.connect(self.print_cns)
            buttons.edit_garde.clicked.connect(self.edit_cns)
            buttons.delete_garde.clicked.connect(self.delete_cns)

            tablerow += 1
        self.table_consultation.setItem(tablerow, 0, QTableWidgetItem(""))
        self.table_consultation.setItem(tablerow, 1, QTableWidgetItem(""))
        self.table_consultation.setItem(tablerow, 2, QTableWidgetItem(""))
        self.table_consultation.setItem(tablerow, 3, QTableWidgetItem(""))
        self.table_consultation.removeCellWidget(tablerow, 4)
        connection.close()

    def edit_cns(self):
        clickme = qApp.focusWidget()
        index = self.table_consultation.indexAt(clickme.parent().pos())
        row = index.row()
        m = self.table_consultation.item(row, 1).text()
        y = self.table_consultation.item(row, 2).text()
        if m == "janvier":
            m = 1
        elif m == "février":
            m = 2
        elif m == "mars":
            m = 3
        elif m == "avril":
            m = 4
        elif m == "mai":
            m = 5
        elif m == "juin":
            m = 6
        elif m == "juillet":
            m = 7
        elif m == "août":
            m = 8
        elif m == "septembre":
            m = 9
        elif m == "octobre":
            m = 10
        elif m == "novembre":
            m = 11
        elif m == "décembre":
            m = 12

        y = int(y)

        self.dentiste_consultation_page = DentisteConsultationUi(m, y)
        self.dentiste_consultation_page.show()
        self.close()

    def delete_cns(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        row = index.row()
        if row > -1:
            id = self.table_gardes.item(row, 0).text()
            connection = sqlite3.connect("database/sqlite.db")
            cur = connection.cursor()
            sql_q = 'DELETE FROM consultaion_mounth WHERE consultation_mounth_id=?'
            cur.execute(sql_q, (id,))
            connection.commit()
            connection.close()
            self.table.setItem(row, 0, QTableWidgetItem(""))
            self.table.setItem(row, 1, QTableWidgetItem(""))
            self.table.setItem(row, 2, QTableWidgetItem(""))
            self.table.setItem(row, 3, QTableWidgetItem(""))
            self.table.setItem(row, 4, QTableWidgetItem(""))
            self.loadGuardMonths()

    def print_cns(self):
        clickme = qApp.focusWidget()
        index = self.table_gardes.indexAt(clickme.parent().pos())
        row = index.row()
        m = self.table_gardes.item(row, 1).text()
        y = self.table_gardes.item(row, 2).text()
        if m == "janvier":
            m = 1
        elif m == "février":
            m = 2
        elif m == "mars":
            m = 3
        elif m == "avril":
            m = 4
        elif m == "mai":
            m = 5
        elif m == "juin":
            m = 6
        elif m == "juillet":
            m = 7
        elif m == "août":
            m = 8
        elif m == "septembre":
            m = 9
        elif m == "octobre":
            m = 10
        elif m == "novembre":
            m = 11
        elif m == "décembre":
            m = 12

        y = int(y)

        self.next_page = export_dentiste_consultation.ExportDentisteConsultationUi(m, y)
        self.close()
        self.next_page.show()

