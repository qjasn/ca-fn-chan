import io

import matplotlib
from flet_core import Image
from matplotlib import pyplot as plt

matplotlib.use("svg")


class MatPlotUi:
    def __init__(self,page):
        self.fig = None
        self.page = page

    def draw(self):
        fig, ax = plt.subplots()
        self.fig = fig
        fruits = ["apple", "blueberry", "cherry", "orange"]
        counts = [40, 100, 30, 55]
        bar_labels = ["red", "blue", "_red", "orange"]
        bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

        ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

        ax.set_ylabel("fruit supply")
        ax.set_title("Fruit supply by kind and color")
        ax.legend(title="Fruit color")
        s = io.StringIO()
        fig.savefig(s, format="svg", transparent=True)
        svg = s.getvalue()
        matplotlib_chart = Image(src=svg, visible=True)
        return matplotlib_chart
