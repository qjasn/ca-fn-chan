import io

from sympy import *
from flet import *

from basic.app_str import UString
from basic.is_dark import is_dark
from matplot.mathtext import math_to_image
import matplotlib.font_manager as mfm

import re
import xml.etree.ElementTree as ET


class EquationUI:
    def __init__(self, page: Page, equ: str, args="x"):
        self.latex_image = None
        self.ui = None
        _solve = ""
        self.equation = equ.replace(" ", "")
        self.page = page
        self.map = {}
        args = args.replace(" ", "")
        for i in args.split(","):
            exec("result = symbols('{}')".format(i))
            self.map[i] = locals()["result"]
        for i in args.split(","):
            _equ = equ.replace(i, 'self.map["{}"]'.format(i))
        self.pares = parse_expr(equ, transformations="all")
        self.latex = latex(self.pares)
        print(str(self.latex))
        for i in args.split(","):
            _solve = _solve + "self.map['{}'],".format(i)
        exec("result = solve(self.pares,({}),dict=True)".format(_solve))
        self.solve = locals()["result"]
        _image = []
        for i in self.solve:
            for a in args.split(","):
                _image.append(self.latex_ui(latex(Eq(self.map[a], i[self.map[a]]))))
        self.solve_img = _image
        self.latex_image = self.latex_ui(self.latex)

    def latex_ui(self, _latex):
        color = "white" if is_dark(self.page) else "black"
        prop = mfm.FontProperties(family='DejaVu Sans Mono', size=64, style="normal")
        _latex = r"${}$".format(_latex)
        s = io.StringIO()
        math_to_image(_latex, s, format="svg", color=color, prop=prop, transparent=True)
        svg = s.getvalue()
        root = ET.fromstring(svg)
        w = float(re.findall(r"\d+", root.attrib["width"])[0])
        h = float(re.findall(r"\d+", root.attrib["height"])[0])
        return Image(src=svg, aspect_ratio=w / h, fit=ImageFit.FILL)

    def on_click(self, _list=None, element=None):
        UString.lists.remove(_list)
        element.content.controls.remove(self.ui)
        self.page.update()

    def create_ui(self, element, _list):
        self.ui = Row(
            [
                Stack([
                    Column(
                        [
                            Row([
                                Container(
                                    content=self.latex_image,
                                    height=15,
                                )
                            ], scroll=ScrollMode.AUTO,
                                width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (
                                        self.page.width - 55),

                            ), Row(
                            [
                                Icon(icons.SUBDIRECTORY_ARROW_RIGHT),
                                Container(
                                    content=Row(
                                        self.solve_img
                                    ),
                                    height=15,
                                )
                            ], scroll=ScrollMode.AUTO,
                            width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (
                                    self.page.width - 55)
                        )
                        ], top=5
                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="删除",
                                on_click=lambda e: self.on_click(_list, element)
                            )
                        ]

                        ), right=0 if self.page.width > 550 else 20,

                    )
                ], width=(((self.page.width - 100) / 7) * 1.8) if self.page.width > 550 else self.page.width,
                    height=50
                )
            ],
            height=50
        )
        return self.ui
