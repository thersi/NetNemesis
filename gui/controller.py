from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog


Form, Window = uic.loadUiType("gui/view.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.button1.setText("Hello World")
window.showMaximized()
app.exec()
