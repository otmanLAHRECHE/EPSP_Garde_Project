import datetime
import sqlite3
import time
from calendar import monthrange
import urgence

from PyQt5 import QtWidgets, uic


class ExportUrgencePlaningUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(ExportUrgencePlaningUi, self).__init__()
        uic.loadUi('ui/export_planing.ui', self)

        self.month = month
        self.year = year

        self.ttl = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.status = self.findChild(QtWidgets.QLabel, "label_2")
        self.export = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.setEnabled(False)
        self.data = [("Jours", "Date", "De 08h:00 à 20h:00", "De 20h:00 à 08h:00")]
        self.num_days = monthrange(self.year, self.month)[1]

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

        self.ttl.setText("Exporté le planing de garde service d urgence " + m + "/" +str(self.year))

        connection = sqlite3.connect('database/sqlite.db')
        cur = connection.cursor()

        for row in range(self.num_days):

            prog = row * 100 / range(self.num_days)
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

            if self.month / 10 > 1:
                date_day = str(day) + "/" + str(self.month) + "/" + str(self.year)
            else:
                date_day = str(day) + "/" + str(0) + str(self.month) + "/" + str(self.year)

            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, ('urgence', 'light', day, self.month, self.year))
            results_light = cur.fetchall()

            sql_q = 'SELECT health_worker.full_name FROM health_worker INNER JOIN guard ON health_worker.worker_id = guard.gardien_id where service=? and guard.periode =? and guard.d =? and guard.m =? and guard.y =?'
            cur.execute(sql_q, ('urgence', 'night', day, self.month, self.year))
            results_night = cur.fetchall()

            light = "Dr/ "
            night = "Dr/ "

            if results_light:
                rl = results_light[0]
                light = light + str(rl[0])

            if results_night:
                rn = results_night[0]
                night = night + str(rn[0])

            data_day = (m, date_day, light, night)

            self.data[day] = data_day

            time.sleep(1)
            self.progress.setValue(prog)

        print(self.data)
        self.export.setEnabled(True)

    def export_pdf(self):
        print(self.data)

        """
        self.next_page = urgence.UrgenceMainUi()
        self.next_page.show()
        self.close()
        """







