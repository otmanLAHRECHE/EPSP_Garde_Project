from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import sys


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)
        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab_gardes = self.findChild(QWidget, "tab")
        self.tab_medcines = self.findChild(QWidget, "tab_2")



