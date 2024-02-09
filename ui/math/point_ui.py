import io
import re
import xml.etree.ElementTree as ET

import matplotlib.font_manager as mfm
from flet import *
from sympy import latex, sympify

from basic.app_str import UString
from basic.is_dark import is_dark
from matplot.latex.mathtext import math_to_image


class PointUI:
    def __init__(self, name: str, x, y, page):
        self.ui = None
        self.name = name
        self.x, self.y = x, y
        self.page = page
        x_latex = str(latex(sympify(x)))
        y_latex = str(latex(sympify(y)))
        self.latex_text = r"{}:({},{})".format(name, x_latex, y_latex)
        self.latex_image = self.latex_ui(self.latex_text)

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
        return [Image(src=svg, aspect_ratio=w / h, fit=ImageFit.FILL), (15 / 58) * h]

    def on_change(self, e):
        UString.draw_class[self.name].visible(e.control.value)
        UString.matplot_chart.update_draw()  # 更新UI
        self.page.update()

    def on_click(self, _list=None, element=None):
        # 该函数在点击 删除 时调用
        UString.lists.remove(_list)  # 从lists删除对应的结构化函数
        UString.draw_class[_list["name"]].delete()  # 清除函数图像
        UString.p_e.remove(_list["name"])  # 删除存在的函数名称
        UString.draw_class.pop(_list["name"])
        element.content.controls.remove(self.ui)  # 从页面删除此元素
        UString.matplot_chart.update_draw()  # 更新UI
        self.page.update()

    def create_ui(self, _list, element):
        # 构建UI
        self.ui = Row(
            [
                Stack([
                    Row([
                        Checkbox(
                            value=True,
                            on_change=self.on_change

                        ),
                        Container(
                            content=self.latex_image[0],
                            height=self.latex_image[1]
                        )
                    ], scroll=ScrollMode.ALWAYS,
                        width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (
                                self.page.width - 55),

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
                )
            ]
        )
        return self.ui
