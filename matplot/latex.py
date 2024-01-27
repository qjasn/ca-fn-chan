import io
import re
import xml.etree.ElementTree as ET

import flet as ft
import latexify
import matplotlib.font_manager as mfm
from flet_core import Image

from basic.is_dark import is_dark
from matplot.mathtext import math_to_image


class Latex:
    def __init__(self, text: str, name: str, args: str, page: ft.Page):
        self.error = False
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
            self.warning("Make sure your symbol in the equation")

    def warning(self, e: str):
        self.error = True
        page = self.page
        page.dialog = ft.AlertDialog(
            title=ft.Text("Please enter a right function"),
            content=ft.Text("stderr:\n{}".format(e)),
            modal=False,
            open=True
        )
        page.update()

    def init(self, subscript=False):
        _name = self.name
        _text = self.text
        _ags = self.args
        _latex = None
        try:
            self.latex = latexify.get_latex_with_code(_name, _ags, _text)
            if subscript:
                self.latex = self.latex.replace("\_", "_")
            self.latex = r"${}$".format(self.latex)
            return self.latex
        except Exception as e:
            if not self.error:
                self.warning(str(e))
                self.error = True
            self.latex = r"ERROR"
            return self.latex

    def output_plain(self):
        print(self.latex)

    def output_svg(self):
        color = "white" if is_dark(self.page) else "black"
        prop = mfm.FontProperties(family='DejaVu Sans Mono', size=64, style="normal")
        string = io.StringIO()
        try:
            math_to_image(self.latex, filename_or_obj=string, format="svg", prop=prop, dpi=128, color=color,
                          transparent=True)
        except Exception as e:
            if not self.error:
                self.warning(str(e))
                self.error = True
            self.latex = r"ERROR"
            math_to_image(self.latex, filename_or_obj=string, format="svg", prop=prop, dpi=128, color=color,
                          transparent=True)
        svg = string.getvalue()
        root = ET.fromstring(svg)
        w = float(re.findall(r"\d+", root.attrib["width"])[0])
        h = float(re.findall(r"\d+", root.attrib["height"])[0])
        return [Image(src=svg, aspect_ratio=w / h, fit=ft.ImageFit.FILL), (17 / 58) * h]
