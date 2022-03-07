from PyQt5 import QtWidgets, uic




class UrgenceGuardUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(UrgenceGuardUi, self).__init__()
        uic.loadUi('ui/guard_urgence.ui', self)

        self.ttl = self.findChild(QtWidgets.QLabel, "label")

        self.month = month
        self.year = year

        print(self.month)
        print(self.year)


        """
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
            """
        # self.ttl.setText("Planing de garde urgence mois " + m + " de l année " + self.year + ":")
