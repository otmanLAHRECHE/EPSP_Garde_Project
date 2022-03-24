import os

from PyQt5 import QtWidgets, uic

import urgence
import urgence_inf

basedir = os.path.dirname(__file__)

class UrgenceChoseUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceChoseUi, self).__init__()

        uic.loadUi(os.path.join(basedir, 'ui', 'urgence_chose.ui'), self)

        self.med = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.infirmier = self.findChild(QtWidgets.QPushButton, "pushButton_3")

        self.med.clicked.connect(self.med_click)
        self.infirmier.clicked.connect(self.infirmier_click)

    def med_click(self):
        self.next_page = urgence.UrgenceMainUi()
        self.next_page.show()
        self.close()

    def infirmier_click(self):


        self.next_page = urgence_inf.UrgenceInfUi()
        self.next_page.show()
        self.close()



