import io
import re
import xml.etree.ElementTree as ET

import flet as ft
import latexify
from flet_core import Image
import matplotlib.font_manager as mfm

from matplot.mathtext import math_to_image


class Latex:
    def __init__(self, text: str, name: str, args: str, page: ft.Page):
        self.export_f = None
        self.page = page
        self.name = name
        self.args = args
        self.latex = None
        _text = "".join(text.split("return")[1].split(" "))
        if all(["=" not in text, args in text]):
            self.text = text
        elif _text.isnumeric():
            self.text = text
        else:
            page.dialog = ft.AlertDialog(
                title=ft.Text("Please enter a right function"),
                modal=False,
                open=True
            )
            page.update()

    def init(self):
        _name = self.name
        _text = self.text
        _ags = self.args
        _latex = None
        self.latex = latexify.get_latex_with_code(_name, _ags, _text)
        self.latex = r"${}$".format(self.latex)
        return self.latex

    def output_plain(self):
        print(self.latex)

    def output_svg(self):
        if self.page.theme_mode == "SYSTEM":
            if self.page.platform_brightness == ft.ThemeMode.DARK:
                color = "white"
            else:
                color = "black"
        elif self.page.theme_mode == "DARK":
            color = "white"
        else:
            color = "black"
        prop = mfm.FontProperties(family='DejaVu Sans Mono', size=64, style="normal")
        string = io.StringIO()
        math_to_image(self.latex, filename_or_obj=string, format="svg", prop=prop, dpi=128, color=color,
                      transparent=True)
        svg = string.getvalue()
        root = ET.fromstring(svg)
        w = float(re.findall(r"\d+", root.attrib["width"])[0])
        h = float(re.findall(r"\d+", root.attrib["height"])[0])
        return Image(src=svg, aspect_ratio=w / h, fit=ft.ImageFit.FILL)
