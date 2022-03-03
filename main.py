


from PyQt5 import uic
from PyQt5.QtWidgets import *

Form, Window = uic.loadUiType("ui/main.ui")
app = QApplication([])
window = Window()
form = Form()






form.setupUi(window)
window.show()
app.exec_()