import sys
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5,4),dpi=100)
        super().__init__(fig)
        self.setParent(parent)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800,600)

        chart = Canvas(self)

app = QApplication(sys.argv)
demo =App()
demo.show()
sys.exit(app.exec_())