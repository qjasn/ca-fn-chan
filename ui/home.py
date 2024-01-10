from matplot.test import MatPlotUi
from flet import *


class HomePage:
    def __init__(self, page):
        self.page = page
        self.lists = []
        self.dialog = AlertDialog(
            modal=True,
            title=Text("Enter the function"),
            content=TextField(label="Function", value="y = x"),
            actions=[
                TextButton("OK", on_click=self.close_dlf)
            ]
        )

    def close_dlf(self, e):
        self.dialog.open = False
        self.page.update()

    def add(self, e):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()


def home_page(_page, navbar):
    math = MatPlotUi(_page)
    matplotlib_chart = math.draw()
    control = HomePage(_page)

    def show_chart(e):
        matplotlib_chart.visible = True
        print(e)
        _page.update()

    input_ui = Column(
        controls=[
            Text("Press the Add button to add a new function", style=TextThemeStyle.BODY_SMALL,
                 text_align=TextAlign.CENTER),
            Divider(),
            Row(
                [
                    IconButton(
                        icon=icons.ADD, on_click=control.add
                    )
                ],
                alignment=MainAxisAlignment.END
            ),
        ],
        expand=True,
        alignment=MainAxisAlignment.START,
    )
    content = [Row(

        [
            navbar,
            VerticalDivider(width=1),
            Row(
                [
                    input_ui
                ],
                width=((_page.width - 100) / 7) * 1.8,
                alignment=MainAxisAlignment.START,
            ),
            VerticalDivider(width=1),
            Row(
                [
                    Container(
                        matplotlib_chart,
                        bgcolor=colors.YELLOW,
                        height=_page.height,
                        expand=True
                    )
                ],
                expand = True,
                alignment=MainAxisAlignment.END
            )
        ], expand=True
    )
    ] if _page.width > 550 else [SafeArea(
        content=Column(
            [
                Column(
                    [
                        Container(
                            matplotlib_chart,
                            bgcolor=colors.YELLOW,
                            width=_page.width,
                            height=((_page.height - 150) / 7) * 4.5
                        ),
                    ]
                ),
                Divider(height=1),
                Column(
                    [
                        input_ui
                    ]),
            ],
        )
    ), navbar]
    View(
        "/home",
        controls=content
    )
    return content
