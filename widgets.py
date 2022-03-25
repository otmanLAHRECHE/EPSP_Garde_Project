from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget



class Buttons(QWidget):
    def __init__(self):
        super(Buttons, self).__init__()

        # add your buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.edit_garde = QtWidgets.QPushButton()
        self.edit_garde.setText("GARDE")
        self.delete_garde = QtWidgets.QPushButton()
        self.delete_garde.setText("Delete")
        self.print_garde = QtWidgets.QPushButton()
        self.print_garde.setText("RECAP")

        button_layout.addStretch(1)
        button_layout.addWidget(self.print_garde)
        button_layout.addWidget(self.edit_garde)
        button_layout.addWidget(self.delete_garde)

        self.setLayout(button_layout)


class Chose_worker(QWidget):
    def __init__(self, list_workers):
        super(Chose_worker, self).__init__()

        widget = QtWidgets.QHBoxLayout()
        self.chose = QtWidgets.QComboBox()
        self.chose.addItem("")
        for worker in list_workers:
            self.chose.addItem(worker[0])
        widget.addWidget(self.chose)

        self.setLayout(widget)


class Buttons_inf(QWidget):
    def __init__(self):
        super(Buttons_inf, self).__init__()

        # add your buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.edit_garde_surv = QtWidgets.QPushButton()
        self.edit_garde_surv.setText("GARDE Surv")
        self.edit_garde_inf = QtWidgets.QPushButton()
        self.edit_garde_inf.setText("GARDE Inf")
        self.delete_garde = QtWidgets.QPushButton()
        self.delete_garde.setText("Delete")
        self.print_garde = QtWidgets.QPushButton()
        self.print_garde.setText("RECAP")

        button_layout.addStretch(1)
        button_layout.addWidget(self.print_garde)
        button_layout.addWidget(self.edit_garde_inf)
        button_layout.addWidget(self.edit_garde_surv)
        button_layout.addWidget(self.delete_garde)

        self.setLayout(button_layout)


class Buttons_rad(QWidget):
    def __init__(self):
        super(Buttons_rad, self).__init__()

        # add your buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.edit_garde = QtWidgets.QPushButton()
        self.edit_garde.setText("GARDE")
        self.edit_state = QtWidgets.QPushButton()
        self.edit_state.setText("STATISTIQUE")
        self.delete_garde = QtWidgets.QPushButton()
        self.delete_garde.setText("Delete")
        self.print_garde = QtWidgets.QPushButton()
        self.print_garde.setText("RECAP")

        button_layout.addStretch(1)
        button_layout.addWidget(self.print_garde)
        button_layout.addWidget(self.edit_state)
        button_layout.addWidget(self.edit_garde)
        button_layout.addWidget(self.delete_garde)

        self.setLayout(button_layout)
