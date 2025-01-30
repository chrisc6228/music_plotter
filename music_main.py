from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import subprocess

def clicked():
    subprocess.run(["python", "music_visualizer.py"])

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 600, 400)
    win.setWindowTitle("Welcome to Spectrogram Music Notator!")

    label = QtWidgets.QLabel(win)
    label.setText("Welcome!")
    label.move(230, 100)
    label.setWordWrap(True)

    b = QtWidgets.QPushButton(win)
    b.setText("notate")
    b.clicked.connect(clicked)
    b.move(230, 200)

    win.show()
    sys.exit(app.exec())

window()