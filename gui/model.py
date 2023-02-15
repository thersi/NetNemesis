from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import QUrl

from robot_sim import robot_simulator

robot_simulator()
Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.simulationView.load(QUrl('http://localhost:52000/?53084'))
form.simulationView.show()
window.showMaximized()
app.exec()
