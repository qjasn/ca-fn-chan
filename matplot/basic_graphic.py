import io
import re
import xml.etree.ElementTree as ET

import matplotlib
from flet_core import Image, ImageFit, Container
from matplotlib import pyplot as plt

from basic.app_str import UString
from basic.tiny_fn import is_dark

matplotlib.use("svg")


class MatPlotUi:
    def __init__(self, page):
        self.plt = None
        self.ax = None
        self.ui = None
        self.fig = None
        self.page = page

    def draw(self, only_clear=False):
        color = "white" if is_dark(self.page) else "black"
        if self.page.width > 550:
            _width = UString.width
            _width = ((_width - 100) / 7) * 5.2
            __width = _width - 50
            _height = UString.height
        else:
            _width = self.page.width
            __width = self.page.width
            _height = ((self.page.height - 150) / 7) * 4.5

        _step = UString.step
        plt.close()
        f_w = __width if __width > _height else _height
        f_h = _height if _height > __width else __width
        plt.figure(figsize=(f_w / 100, f_h / 100))
        self.ax = plt.subplot()

        self.ax.spines[["left", "bottom"]].set_position(("data", 0))
        self.ax.spines[["left", "bottom"]].set_color(color)
        # Hide the top and right spines.
        self.ax.spines[["top", "right"]].set_visible(False)
        self.ax.grid(linewidth=0.3)
        plt.xticks(color=color)
        plt.yticks(color=color)
        x1, x2, y1, y2 = -(_width / _step) / 2, (_width / _step) / 2, -(_height / _step) / 2, (_height / _step) / 2
        self.ax.axis([x1, x2, y1, y2])
        """
        
        plt.xticks(ticks=[x for x in np.linspace(int(-(_width / _step) / 2) - 1,
                                                      int((_width / _step) / 2) + 1, num=int(_width / _step / 2))])
        plt.yticks(ticks=[x for x in np.linspace(int(-(_height / _step) / 2) - 1,
                                                      int((_height / _step) / 2) + 1, num=int(_height / _step / 2))])
        
        """
        x_ticks = []
        i = 0
        while i <= x2:
            x_ticks.append(i)
            i += 2
        i = 0
        while i >= x1:
            x_ticks.append(i)
            i -= 2
        plt.xticks(ticks=x_ticks)
        y_ticks = []
        i = 0
        while i <= y2:
            y_ticks.append(i)
            i += 2
        i = 0
        while i >= y1:
            y_ticks.append(i)
            i -= 2
        plt.yticks(ticks=y_ticks)
        s = io.StringIO()
        plt.savefig(s, format="svg", transparent=True)
        svg = s.getvalue()
        root = ET.fromstring(svg)
        w = float(re.findall(r"\d+", root.attrib["width"])[0])
        h = float(re.findall(r"\d+", root.attrib["height"])[0])
        if only_clear:
            self.ui.content = Image(svg, aspect_ratio=w / h, fit=ImageFit.COVER)
            self.ui.height = _height
            self.ui.width = __width
        else:
            self.ui = Container(
                Image(svg, aspect_ratio=w / h, fit=ImageFit.COVER),
                height=_height,
                width=__width
            )
        self.plt = plt
        return self.ui

    def return_ax(self):
        return self.ax

    async def update_draw(self):
        display_step = UString.display_step
        color = "white" if is_dark(self.page) else "black"
        if self.page.width > 550:
            _width = UString.width
            _width = ((_width - 100) / 7) * 5.2
            __width = _width - 50
            _height = UString.height
        else:
            _width = self.page.width
            __width = self.page.width
            _height = ((self.page.height - 150) / 7) * 4.5
        _step = UString.step
        self.ax.spines[["left", "bottom"]].set_color(color)
        self.ax.spines[["left", "bottom"]].set_position(("data", 0))
        # Hide the top and right spines.
        self.ax.spines[["top", "right"]].set_visible(False)
        self.ax.grid(linewidth=0.3)
        plt.xticks(color=color)
        plt.yticks(color=color)
        x1, x2, y1, y2 = -(_width / _step) / 2, (_width / _step) / 2, -(_height / _step) / 2, (_height / _step) / 2
        x1 += UString.x_offset
        x2 += UString.x_offset
        y1 += UString.y_offset
        y2 += UString.y_offset
        self.ax.axis([x1, x2, y1, y2])
        x_ticks = []
        i = 0
        while i <= x2:
            x_ticks.append(i)
            i += display_step
        i = 0
        while i >= x1:
            x_ticks.append(i)
            i -= display_step
        plt.xticks(ticks=x_ticks)
        y_ticks = []
        i = 0
        while i <= y2:
            y_ticks.append(i)
            i += display_step
        i = 0
        while i >= y1:
            y_ticks.append(i)
            i -= display_step
        plt.yticks(ticks=y_ticks)
        plt.xticks(color=color)
        plt.yticks(color=color)
        s = io.StringIO()
        plt.savefig(s, format="svg", bbox_inches="tight", transparent=True)
        svg = s.getvalue()
        root = ET.fromstring(svg)
        w = float(re.findall(r"\d+", root.attrib["width"])[0])
        h = float(re.findall(r"\d+", root.attrib["height"])[0])
        self.ui.content = Image(svg, aspect_ratio=w / h, fit=ImageFit.COVER)
        self.ui.height = _height
        self.ui.width = __width
        self.plt = plt
        try:
            await self.ui.update_async()
            return self.ui
        except Exception:
            return self.ui

    def get_pic(self, format="svg") -> bytes | str:
        color = "black"
        plt.xticks(color=color)
        self.ax.spines[["left", "bottom"]].set_color(color)
        plt.yticks(color=color)
        if format == "svg":
            s = io.StringIO
        else:
            s = io.BytesIO()
        self.plt.savefig(s, format=format, bbox_inches="tight")
        pic = s.getvalue()
        color = "white" if is_dark(self.page) else "black"
        plt.xticks(color=color)
        self.ax.spines[["left", "bottom"]].set_color(color)
        plt.yticks(color=color)
        return pic
