import numpy as np

import matplot.define_user_function
import matplot.basic_graphic
from basic.app_str import UString
from matplot.define_user_function import DefineUserFunction


class DrawUserFunction:
    def __init__(self, function, page):
        self.plot = None
        self.function = function
        self.name = function["name"]
        self.page = page

    def draw(self):
        ax = UString.matplot_chart.return_ax()
        if self.page.width > 550:
            _width = UString.width
            _width = ((_width - 100) / 7) * 5.2
            __width = _width - 50
            _height = UString.height
        else:
            _width = self.page.width
            __width = self.page.width
            _height = ((self.page.height - 150) / 7) * 4.5
        x1, x2, y1, y2 = -(_width / UString.step) / 2, (_width / UString.step) / 2, -(_height / UString.step) / 2, (
                _height / UString.step) / 2
        x = np.linspace(int(x1) - 1, int(x2) + 1, int(_width))
        y = []
        arg = self.function["args"].split(",")[0].replace(" ", "")
        for i in x:
            y.append(DefineUserFunction().exec(self.function["name"], {arg: i}))
        self.plot = ax.plot(x, y)[-1]

    def delete(self):
        self.plot.remove()

    def visible(self, _bool):
        self.plot.set_visible(_bool)
        self.page.update()
