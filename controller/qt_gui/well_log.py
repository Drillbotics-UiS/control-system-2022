import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsScene

from data_models.plot_path_2d import PlotPath2d


class WellLog(QGraphicsScene):
    def __init__(self, hlines_tuple, background_color: str):
        super().__init__()
        self.figure = plt.figure(facecolor=background_color)
        self.num_of_plots = len(hlines_tuple)

        self.plot_paths: list[PlotPath2d] = []
        for _ in range(self.num_of_plots):
            a = PlotPath2d()
            self.plot_paths.append(a)

        legend = self.figure.add_subplot(411)
        self.ax = self.figure.add_subplot(5, 1, (2, 5))
        self.ax.set_facecolor(background_color)

        self.ax.set_ylim(1000)
        self.ax.set_xlim(0, 1)
        # ROP, WOB, Torque, Pump pressure, MSE

        for i, (col, txt) in enumerate(hlines_tuple):
            legend.text(0, 0.2 - i, "0", color=col)
            legend.text(0.5, 0.2 - i, txt, color=col, ha="center")
            legend.text(1, 0.2 - i, "max", color=col, ha="right")
            legend.hlines(-i, 0, 1, colors=(col,))
        legend.axis("off")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        legend.set_xlim(0, 1)
        legend.set_ylim(-self.num_of_plots, 1)

        # mplstyle.use('fast')
        canvas = matplotlib.backends.backend_qtagg.FigureCanvasQTAgg(self.figure)
        self.proxy_widget = self.addWidget(canvas)

        self.depth = 0
        self.last_depth = 0
        self.colors = [l[0] for l in hlines_tuple]

        self.line_list = []
        for j, value in enumerate(self.plot_paths):
            line, = self.ax.plot(value.x, value.y, color=self.colors[j])
            self.line_list.append(line)

    # updates the plotted lines with the newly updated arrays
    def __update_plot_lines(self):
        for i, line in enumerate(self.line_list):
            line.set_xdata(self.plot_paths[i].x)
            line.set_ydata(self.plot_paths[i].y)
        self.figure.canvas.update()
        self.figure.canvas.flush_events()

    def update_plot(self, value, depth):
        if type(value) is not tuple or len(value) != len(self.plot_paths):
            raise ValueError("expected either all values in a tuple.")

        # adds a point to the arrays that are plotted
        for i, plot_path in enumerate(self.plot_paths):
            plot_path.add_point(value[i], depth)

        self.__update_plot_lines()

    def resize(self, size: QtCore.QSizeF):
        self.proxy_widget.resize(size)
