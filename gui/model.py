from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import QUrl
from controller import controller
from gui.arm_sim.robot_toolbox import robot_simulator
from xbox_controller import XboxController


robot_simulator()
Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.simulationView.load(QUrl('http://localhost:52000/?53084'))
form.simulationView.show()
# controller(form, XboxController)
window.showMaximized()
app.exec()
