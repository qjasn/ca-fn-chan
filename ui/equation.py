from flet_core import *

from lib.app_str import UString
from matplot.latex import Latex


class EquationUI:
    delete = []

    def __init__(self, name, args, text, page):
        self.lists = UString.lists
        self.ui = None
        self.equation = {
            "name": name,
            "args": args,
            "text": text
        }
        self.page = page
        self.latex = Latex(name=name, args=args, text=text, page=page)
        self.latex.init()
        self.latex_image = self.latex.output_svg()

    def on_change(self, e):
        print(e)

    def create_ui(self, _list, element):
        self.ui = Row(
            [
                Stack([
                    Row([
                        Checkbox(
                            value=True,
                            on_change=self.on_change

                        ),
                        Container(
                            content=self.latex_image,
                            height=20
                        )
                    ], scroll=ScrollMode.ALWAYS,
                        width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (
                                self.page.width - 55),

                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="Delete",
                                on_click=lambda e: (
                                    UString.lists.remove(_list),
                                    UString.a_e.remove(_list["name"]),
                                    element.content.controls.remove(self.ui),
                                    self.page.update())
                            )
                        ]

                        ), right=0 if self.page.width > 550 else 20,

                    )
                ], width=(((self.page.width - 100) / 7) * 1.8) if self.page.width > 550 else self.page.width,
                )
            ]
        )
        return self.ui
