import matplotlib.pyplot as plt
from PyQt5.QtCore import QSizeF
from PyQt5.QtWidgets import QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from data_models.path_models import SafetyMarginSurface
from data_models.plot_path_3d import PlotPath3d


class Plotter3D(QGraphicsScene):
    def __init__(self, background_color: str):
        super().__init__()
        self.figure = plt.figure(facecolor=background_color)
        self.ax = self.figure.add_subplot(111, projection="3d")
        self.ax.axes.set_xlim3d(-30, 30)
        self.ax.axes.set_ylim3d(-30, 30)
        self.ax.axes.set_zlim3d(-60, 0)
        self.ax.set_facecolor(background_color)

        canvas = FigureCanvasQTAgg(self.figure)
        self.proxy_widget = self.addWidget(canvas)
        self.prev_value = None
        self.red_line_points = None

        self.drill_path = PlotPath3d()

        self.line, = self.ax.plot(self.drill_path.x, self.drill_path.y, self.drill_path.z, color="#000000")

    def __update_plot_line(self):
        self.line.set_xdata(self.drill_path.x)
        self.line.set_ydata(self.drill_path.y)
        self.line.set_3d_properties(self.drill_path.z)
        self.figure.canvas.update()
        self.figure.canvas.flush_events()

    def update_plot(self, x, y, z):
        self.drill_path.add_point(x, y, z)
        self.__update_plot_line()

    def plot_safety_margin_surface(self, sms: SafetyMarginSurface):
        self.ax.plot_surface(*sms.to_plot, alpha=0.2, color="#ff0000")

    def resize(self, size: QSizeF):
        self.proxy_widget.resize(size)
