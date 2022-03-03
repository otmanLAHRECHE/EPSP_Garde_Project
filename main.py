


from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import sys


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.urgence = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.dentist = self.findChild(QtWidgets.QPushButton, "pushButton_3")
        self.radio = self.findChild(QtWidgets.QPushButton, "pushButton_2")
        self.labo = self.findChild(QtWidgets.QPushButton, "pushButton_4")
        self.pharm = self.findChild(QtWidgets.QPushButton, "pushButton_5")

        self.urgence.clicked.connect(self.urg)
        self.dentist.clicked.connect(self.den)
        self.radio.clicked.connect(self.rad)
        self.labo.clicked.connect(self.lab)
        self.pharm.clicked.connect(self.pha)



        self.show()

    def urg(self):
        print("urgence")

    def rad(self):
        print("radio")

    def den(self):
        print("dentist")

    def lab(self):
        print("lab")

    def pha(self):
        print("pharm")


app = QApplication(sys.argv)
window = MainUi()
app.exec_()