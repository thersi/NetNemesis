from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

Form, Window = uic.loadUiType("gui\interface.ui")

app = QApplication([])
app.setStyleSheet("interface.qss")
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec()
