from basic.app_str import UString
from matplot.function.define_user_function import DefineUserFunction
from sympy import *


class DrawUserFunction:
    def __init__(self, content, page, mode="fx"):
        self.plot = None
        self.content = content
        self.mode = mode
        if mode == "fx":
            self.name = content["name"]
        self.page = page

    def x_range(self, start, end, item: int):
        _step = (end - start) / item
        output = [start]
        for i in range(0, item):
            output.append(start + i * _step)
        return output

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
        if self.mode == "fx":
            x1, x2, y1, y2 = -(_width / UString.step) / 2, (_width / UString.step) / 2, -(_height / UString.step) / 2, (
                    _height / UString.step) / 2
            x = self.x_range(int(x1) - 1, int(x2) + 1, int(_width))
            y = []
            arg = self.content["args"].split(",")[0].replace(" ", "")
            for i in x:
                y.append(DefineUserFunction().exec(self.content["name"], {arg: i}))
            self.plot = ax.plot(x, y)[-1]

        elif self.mode == "point":
            x = float(self.content["x"])
            y = float(self.content["y"])
            self.plot = ax.scatter(x, y)
            ax.spines[["left", "bottom"]].set_position(("data", 0))
            ax.spines[["top", "right"]].set_visible(False)
        elif self.mode == "list":
            x = self.content["x"]
            y = self.content["y"]
            self.plot = ax.plot(x, y)[-1]
        else:
            x, y = [0], [0]

    def delete(self):
        self.plot.remove()

    def visible(self, _bool):
        self.plot.set_visible(_bool)
        self.page.update()
