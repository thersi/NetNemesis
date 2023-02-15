from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from controller import Controller

Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
Controller(form)
window.showMaximized()
app.exec()
