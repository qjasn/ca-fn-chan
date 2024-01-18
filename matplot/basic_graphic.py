import io
import re

import xml.etree.ElementTree as ET

import matplotlib
import numpy as np
from flet_core import Image, ImageFit, Container
from matplotlib import pyplot as plt

from basic.app_str import UString
from basic.is_dark import is_dark

matplotlib.use("svg")


class MatPlotUi:
    def __init__(self, page):
        self.fig = None
        self.page = page

    def draw(self):
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
        ax = plt.subplot()

        ax.spines[["left", "bottom"]].set_position(("data", 0))
        ax.spines[["left", "bottom"]].set_color(color)
        # Hide the top and right spines.
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(linewidth=0.3)
        plt.xticks(color=color)
        plt.yticks(color=color)
        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        x1, x2, y1, y2 = int(-(_width / _step) / 2) - 1, int((_width / _step) / 2) + 1, int(
            -(_height / _step) / 2) - 1, int((_height / _step) / 2) + 1
        ax.axis([x1, x2, y1, y2])
        """
        
        plt.xticks(ticks=[x for x in np.linspace(int(-(_width / _step) / 2) - 1,
                                                      int((_width / _step) / 2) + 1, num=int(_width / _step / 2))])
        plt.yticks(ticks=[x for x in np.linspace(int(-(_height / _step) / 2) - 1,
                                                      int((_height / _step) / 2) + 1, num=int(_height / _step / 2))])
        """
        xticks = []
        i = 0
        while i <= x2:
            xticks.append(i)
            i += 2
        i = 0
        while i >= x1:
            xticks.append(i)
            i -= 2
        plt.xticks(ticks=xticks)
        yticks = []
        i = 0
        while i <= y2:
            yticks.append(i)
            i += 2
        i = 0
        while i >= y1:
            yticks.append(i)
            i -= 2
        plt.yticks(ticks=yticks)
        s = io.StringIO()
        plt.savefig(s, format="svg", bbox_inches="tight", transparent=True)
        svg = s.getvalue()
        root = ET.fromstring(svg)
        w = float(re.findall(r"\d+", root.attrib["width"])[0])
        h = float(re.findall(r"\d+", root.attrib["height"])[0])
        print(_width)
        return Container(
            Image(svg, aspect_ratio=w / h, fit=ImageFit.COVER),
            height=_height,
            width=__width
        )
