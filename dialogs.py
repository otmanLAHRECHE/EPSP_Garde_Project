from PyQt5 import QtWidgets, uic


class Login_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Login_dialog, self).__init__()
        uic.loadUi('ui/login_dialog.ui', self)
        self.setWindowTitle("login")
        self.username = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.password = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")


class Update_worker_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Update_worker_dialog, self).__init__()
        uic.loadUi('ui/update_worker_name.ui', self)
        self.setWindowTitle("metre a jour")
        self.worker = self.findChild(QtWidgets.QLineEdit, "lineEdit")


class Add_new_month(QtWidgets.QDialog):
    def __init__(self):
        super(Add_new_month, self).__init__()
        uic.loadUi('ui/add_new_month.ui', self)
        self.setWindowTitle("ajouter nouveau planing")
        self.month = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.year = self.findChild(QtWidgets.QLineEdit, "lineEdit")
