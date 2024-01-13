from flet_core import *

from matplot.latex import Latex


class EquationUI:
    def __init__(self, name, args, text, page):
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
        print("On Change")
        print(self)

    def create_ui(self):
        return Row(
            [
                Stack([
                    Row([
                        Checkbox(
                            value=True,
                            on_change=self.on_change,

                        ),
                        Container(
                            content=self.latex_image,
                            height=15
                        )
                    ], scroll=ScrollMode.ALWAYS,
                        width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (self.page.width - 55),

                    ),
                    Container(
                        content=IconButton(
                            icon=icons.MORE_HORIZ,
                            icon_size=20,
                            height=35,
                            width=35
                        ),
                        right=0 if self.page.width > 550 else 20,
                    )
                ], width=(((self.page.width - 100) / 7) * 1.8) if self.page.width > 550 else self.page.width,
                )
            ]
        )
