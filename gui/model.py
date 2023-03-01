from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from controller import Controller
from PyQt6.QtCore import QUrl
from xbox_controller import XboxController

Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.simulationView.load(QUrl('http://localhost:52000/?53084'))
form.simulationView.show()
Controller(form)
window.showMaximized()
app.exec()
