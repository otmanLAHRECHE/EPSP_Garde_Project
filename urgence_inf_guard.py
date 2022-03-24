
import os

from PyQt5 import QtWidgets, uic

basedir = os.path.dirname(__file__)

class UrgenceInfGuardUi(QtWidgets.QMainWindow):
    def __init__(self, month, year):
        super(UrgenceInfGuardUi, self).__init__()
        uic.loadUi(os.path.join(basedir, 'ui', 'urgence_inf_guard.ui'), self)