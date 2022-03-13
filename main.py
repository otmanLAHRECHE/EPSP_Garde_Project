


from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import sys

from dentiste import DentisteMainUi
from dialogs import Login_dialog
from tools import create_garde_page
from urgence import UrgenceMainUi
from urgence_guard import UrgenceGuardUi


class MainUi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainUi, self).__init__()
        uic.loadUi('ui/main.ui', self)



        self.epsp = self.findChild(QtWidgets.QLabel, "label")
        self.choisir = self.findChild(QtWidgets.QLabel, "label_2")

        self.choisir.setContentsMargins(40, 0, 5, 0)

        self.grid = self.findChild(QtWidgets.QGridLayout, "gridLayout")
        self.urgence = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.dentist = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.radio = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.labo = self.findChild(QtWidgets.QPushButton, "pushButton_4")
        self.pharm = self.findChild(QtWidgets.QPushButton, "pushButton_5")
        self.resp = self.findChild(QtWidgets.QLabel, "label_3")

        self.grid.addWidget(self.urgence, 1, 1)
        self.grid.addWidget(self.dentist, 1, 2)
        self.grid.addWidget(self.radio, 1, 3)
        self.grid.addWidget(self.labo, 2, 1)
        self.grid.addWidget(self.pharm, 2, 2)
        self.resp.setText("")

        self.urgence.clicked.connect(self.urg)
        self.dentist.clicked.connect(self.den)
        self.radio.clicked.connect(self.rad)
        self.labo.clicked.connect(self.lab)
        self.pharm.clicked.connect(self.pha)



    def urg(self):
        dialog = Login_dialog()

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.username.text() == "urgence" and dialog.password.text() == "urgence":
                self.resp.setText("authentifié")
                self.urgencepage = UrgenceMainUi()
                self.urgencepage.show()
                self.close()

            else:
                self.resp.setText("nom utilisateur ou mods de pass erroné")
        print("urgence")

    def rad(self):
        print("radio")

    def den(self):
        dialog = Login_dialog()

        if dialog.exec() == QtWidgets.QDialog.Accepted:
            if dialog.username.text() == "dentiste" and dialog.password.text() == "dentiste":
                self.resp.setText("authentifié")
                self.urgencepage = DentisteMainUi()
                self.urgencepage.show()
                self.close()

            else:
                self.resp.setText("nom utilisateur ou mods de pass erroné")

    def lab(self):
        print("lab")

    def pha(self):
        print("pharm")


def main():
    app = QApplication(sys.argv)
    window = MainUi()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
