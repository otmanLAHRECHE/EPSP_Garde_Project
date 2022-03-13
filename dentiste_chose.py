from PyQt5 import QtWidgets, uic

import dentiste
import infirmier


class DentisteChoseUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(DentisteChoseUi, self).__init__()
        uic.loadUi('ui/dentiste_chose.ui', self)


        self.dentiste = self.findChild(QtWidgets.QPushButton, "pushButton")
        self.infirmier = self.findChild(QtWidgets.QPushButton, "pushButton_2")

        self.dentiste.clicked.connect(self.dentiste_click)
        self.infirmier.clicked.connect(self.infirmier_click)


    def dentiste_click(self):
        self.next_page = dentiste.DentisteMainUi()
        self.next_page.show()
        self.close()

    def infirmier_click(self):
        self.next_page = infirmier.InfermierMainUi()
        self.next_page.show()
        self.close()

