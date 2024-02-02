from basic.app_str import UString


class DrawUserPoint:
    def __init__(self, x, y):
        self.plot = None
        self.x = x
        self.y = y

    def p_draw(self):
        ax = UString.matplot_chart.return_ax()
        self.plot = ax.plot([self.x], [self.y], "o")[-1]

    def visible(self, _bool):
        self.plot.set_visible(_bool)

    def delete(self):
        self.plot.remove()
