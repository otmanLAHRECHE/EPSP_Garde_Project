import os
import sqlite3

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QPushButton, QTableWidget, QMessageBox, QTableWidgetItem, qApp

from dialogs import Add_new_inf, Saving_progress_dialog, Add_new_month, Update_worker_dialog
from threads import ThreadAddGroupe, ThreadUpdateGroupe
from tools import get_workers_count, get_guard_months_count
from widgets import Buttons_inf

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
        self.table_gardes.setColumnWidth(4, 330)
        self.table_gardes.hideColumn(0)

        self.loadGuardMonths()
        self.loadUsers()
        self.loadGroups()

        self.add.clicked.connect(self.add_toDb)
        self.delete.clicked.connect(self.deleteUser)
        self.update.clicked.connect(self.updateUser)
        self.add_garde.clicked.connect(self.add_grd)

        self.add_group.clicked.connect(self.add_to_groupe)
        self.delete_group.clicked.connect(self.deleteUser_group)
        self.update_group.clicked.connect(self.updateUserGroupe)



    def alert_(self, message):
        alert = QMessageBox()
        alert.setWindowTitle("alert")
        alert.setText(message)
        alert.exec_()

    def add_toDb(self):
        med_count = get_workers_count("urgence_surv")[0]
        if self.medcinname.text() == "":
            message = 'Le champ de nom est vide!'
            self.alert_(message)

        elif med_count[0] > 25:
            message = 'Maximum nombre des inf, supremer un inf'
            self.alert_(message)
        else:

            connection = sqlite3.connect("database/sqlite.db")
            cur = connection.cursor()
            sql_q = "INSERT INTO health_worker (full_name,service) values (?,?)"
            med = (self.medcinname.text(), 'urgence_surv')
            cur.execute(sql_q, med)
            connection.commit()
            connection.close()
            self.medcinname.setText("")
            self.loadUsers()

    def add_to_groupe(self):
        med_count = get_workers_count("urgence_inf")[0]
        dialog_add = Add_new_inf()
        if dialog_add.exec() == QtWidgets.QDialog.Accepted:
            if dialog_add.nom == "":
                message = 'Le champ de nom est vide!'
                self.alert_(message)
            elif med_count[0] > 25:
                message = 'Maximum nombre des inf, supremer un inf'
                self.alert_(message)
            else:
                self.dialog = Saving_progress_dialog()
                self.dialog.label.setText("saving")
                self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.dialog.show()

                self.thr = ThreadAddGroupe(dialog_add.nom.text(), dialog_add.groupe.currentText())
                self.thr._signal.connect(self.signal_accepted)
                self.thr._signal_result.connect(self.signal_accepted)
                self.thr.start()

    def add_grd(self):

        guards_months_count = get_guard_months_count("urgence_sur_inf")[0]

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

                guard_m = (m, int(dialog.year.text()), 'urgence_sur_inf')
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
            message = 'Selectioner un inf'
            self.alert_(message)

    def deleteUser_group(self):
        row = self.table_group.currentRow()
        if row > -1:
            id = self.table_group.item(row, 0).text()
            connection = sqlite3.connect("database/sqlite.db")
            cur = connection.cursor()
            sql_q = 'DELETE FROM health_worker WHERE worker_id=?'
            cur.execute(sql_q, (id,))

            sql_q = 'DELETE FROM groupe WHERE inf_id=?'
            cur.execute(sql_q, (id,))

            connection.commit()
            connection.close()
            self.table_group.setItem(row, 0, QTableWidgetItem(""))
            self.table_group.setItem(row, 1, QTableWidgetItem(""))
            self.table_group.setItem(row, 2, QTableWidgetItem(""))
            self.table_group.setItem(row, 3, QTableWidgetItem(""))
            self.loadGroups()
        else:
            message = 'Selectioner un inf'
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
            message = 'Selectioner un inf'
            self.alert_(message)

    def updateUserGroupe(self):
        row = self.table_group.currentRow()
        if row > -1:
            id = self.table_group.item(row, 0).text()
            name = self.table_group.item(row, 1).text()
            groupe = self.table_group.item(row, 3).text()

            dialog = Add_new_inf()
            dialog.setWindowTitle("Update infirmier")
            dialog.nom.setText(name)
            dialog.groupe.setCurrentText(groupe)
            dialog.ttl.setText("metre a jour l'infirmier :")
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                if dialog.nom.text() == "":
                    message = "enter un valide nom"
                    self.alert_(message)
                elif dialog.nom.text() == name and dialog.groupe.currentText() == groupe:
                    print("do nothing")
                elif dialog.nom.text() == name:
                    self.dialog = Saving_progress_dialog()
                    self.dialog.label.setText("saving")
                    self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.dialog.show()
                    self.thr1 = ThreadUpdateGroupe(id, "", dialog.groupe.currentText())
                    self.thr1._signal.connect(self.signal_accepted_update)
                    self.thr1._signal_result.connect(self.signal_accepted_update)
                    self.thr1.start()
                elif dialog.groupe == groupe:
                    self.dialog = Saving_progress_dialog()
                    self.dialog.label.setText("saving")
                    self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.dialog.show()
                    self.thr1 = ThreadUpdateGroupe(id, dialog.nom.text(), "")
                    self.thr1._signal.connect(self.signal_accepted_update)
                    self.thr1._signal_result.connect(self.signal_accepted_update)
                    self.thr1.start()
                else:
                    self.dialog = Saving_progress_dialog()
                    self.dialog.label.setText("saving")
                    self.dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    self.dialog.show()
                    self.thr1 = ThreadUpdateGroupe(id, dialog.nom.text(), dialog.groupe.currentText())
                    self.thr1._signal.connect(self.signal_accepted_update)
                    self.thr1._signal_result.connect(self.signal_accepted_update)
                    self.thr1.start()

            self.loadGroups()
        else:
            message = 'Selectioner un inf'
            self.alert_(message)

    def loadUsers(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT * FROM health_worker where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence_surv',))
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

    def loadGroups(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT health_worker.worker_id, health_worker.full_name, health_worker.service, groupe.g  FROM health_worker INNER JOIN groupe ON health_worker.worker_id = groupe.inf_id where health_worker.service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence_inf',))
        results = cur.fetchall()
        for row in results:
            self.table_group.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.table_group.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.table_group.setItem(tablerow, 2, QTableWidgetItem(row[2]))
            self.table_group.setItem(tablerow, 3, QTableWidgetItem(row[3]))
            tablerow += 1
        self.table_group.setItem(tablerow, 0, QTableWidgetItem(""))
        self.table_group.setItem(tablerow, 1, QTableWidgetItem(""))
        self.table_group.setItem(tablerow, 2, QTableWidgetItem(""))
        self.table_group.setItem(tablerow, 3, QTableWidgetItem(""))
        connection.close()




    def signal_accepted(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            print(progress)
            self.dialog.close()
            self.loadGroups()

    def signal_accepted_update(self, progress):
        if type(progress) == int:
            self.dialog.progress.setValue(progress)
        elif type(progress) == bool:
            self.dialog.progress.setValue(100)
            self.dialog.label.setText("complete")
            print(progress)
            self.dialog.close()
            self.loadGroups()


    def loadGuardMonths(self):
        connection = sqlite3.connect("database/sqlite.db")
        cur = connection.cursor()
        sql_q = 'SELECT * FROM guard_mounth where service=?'
        tablerow = 0
        cur.execute(sql_q, ('urgence_sur_inf',))
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
            buttons = Buttons_inf()
            self.table_gardes.setCellWidget(tablerow, 4, buttons)
            buttons.print_garde.clicked.connect(self.print_g)
            buttons.edit_garde_inf.clicked.connect(self.edit_g_inf)
            buttons.edit_garde_surv.clicked.connect(self.edit_g_surv)
            buttons.delete_garde.clicked.connect(self.delete_g)

            tablerow += 1
        self.table_gardes.setItem(tablerow, 0, QTableWidgetItem(""))
        self.table_gardes.setItem(tablerow, 1, QTableWidgetItem(""))
        self.table_gardes.setItem(tablerow, 2, QTableWidgetItem(""))
        self.table_gardes.setItem(tablerow, 3, QTableWidgetItem(""))
        self.table_gardes.removeCellWidget(tablerow, 4)
        connection.close()

    def edit_g_inf(self):
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

        """
        self.urgence_guard_page = urgence_guard.UrgenceGuardUi(m, y)
        self.urgence_guard_page.show()
        self.close()
        """

    def edit_g_surv(self):
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

        """
        self.urgence_guard_page = urgence_guard.UrgenceGuardUi(m, y)
        self.urgence_guard_page.show()
        self.close()
        """

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

        """
        self.next_page = recap.RecapUi(m, y, "urgence")
        self.close()
        self.next_page.show()
        """







