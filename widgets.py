from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget


class Buttons(QWidget):
    def __init__(self):
        super(Buttons, self).__init__()

        # add your buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.edit_garde = QtWidgets.QPushButton()
        self.edit_garde.setText("edit")
        self.delete_garde = QtWidgets.QPushButton()
        self.delete_garde.setText("delete")
        self.print_garde = QtWidgets.QPushButton()
        self.print_garde.setText("print")

        button_layout.addStretch(1)
        button_layout.addWidget(self.print_garde)
        button_layout.addWidget(self.edit_garde)
        button_layout.addWidget(self.delete_garde)

        self.setLayout(button_layout)


class Chose_worker(QWidget):
    def __init__(self):
        super(Chose_worker, self).__init__()

        widget = QtWidgets.QHBoxLayout()
        self.chose = QtWidgets.QComboBox()
        self.chose.addItem("hamdi")
        widget.addWidget(self.chose)

        self.setLayout(widget)
