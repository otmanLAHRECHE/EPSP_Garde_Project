from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialogButtonBox, QVBoxLayout, QLabel


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


class CustomDialog(QtWidgets.QDialog):
    def __init__(self, msg, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Alert")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Saving_progress_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Saving_progress_dialog, self).__init__()
        uic.loadUi('ui/saving_dialog.ui', self)

        self.label = self.findChild(QtWidgets.QLabel, "label")
        self.progress = self.findChild(QtWidgets.QProgressBar, "progressBar")
        self.progress.setValue(0)
