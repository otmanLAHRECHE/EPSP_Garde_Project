from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import sys


class UrgenceMainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(UrgenceMainUi, self).__init__()
        uic.loadUi('ui/urgence.ui', self)
        self.tab = self.findChild(QtWidgets.QTabWidget, "tabWidget")

        self.tab_gardes = QWidget()
        self.tab_medcines = QWidget()

        self.tab.addTab(self.tab_gardes, "Listes de Garde")
        self.tab.addTab(self.tab_medcines, "Medcines")


