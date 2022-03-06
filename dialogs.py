from PyQt5 import QtWidgets, uic


class Login_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Login_dialog, self).__init__()
        uic.loadUi('ui/login_dialog.ui', self)
        self.username = self.findChild(QtWidgets.QLineEdit, "lineEdit")
        self.password = self.findChild(QtWidgets.QLineEdit, "lineEdit_2")


class Update_worker_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Update_worker_dialog, self).__init__()
        uic.loadUi('ui/update_worker_name.ui', self)
        self.worker = self.findChild(QtWidgets.QLineEdit, "lineEdit")
