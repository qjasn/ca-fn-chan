from flet import *

from basic.app_str import UString
from matplot.basic_graphic import MatPlotUi
from matplot.draw_user_function import DrawUserFunction
from ui.add_math import AddMath


class MainPage:
    s_index = 0

    def __init__(self, page):
        self.matplot_chart = None
        UString.matplot_chart = MatPlotUi(page)
        self.lists = UString.lists
        self.page = page

    def matplot_ui(self):
        # 从全局变量中构建函数图像的UI，该方法在初始化/页面分辨率改变时会触发
        print(UString.lists)
        for content in UString.lists:
            DrawUserFunction(content, self.page).draw(UString.matplot_chart.return_ax())
            UString.matplot_chart.update_draw()
        self.matplot_chart = UString.matplot_chart.update_draw()
        return self.matplot_chart

    def nav_change(self):
        return self.matplot_chart


def main_page(_page, navbar):
    print(UString.width)
    equals = Container()  # latex公式
    if any([UString.main_page_control is None, UString.math_list is None]):
        UString.main_page_control = MainPage(_page)
        UString.math_list = AddMath(_page, equals)
    _control = UString.main_page_control
    if all([UString.nav_change, not UString.change_dark]):
        matplot_chart = _control.nav_change()
        equals.content = UString.math_list.create_ui()
    else:
        UString.main_page_control = MainPage(_page)
        UString.math_list = AddMath(_page, equals)
        _control = UString.main_page_control
        equals.content = UString.math_list.create_ui()
        UString.matplot_chart.draw()
        matplot_chart = _control.matplot_ui()  # 函数图像UI

    def add(e, mode="fx"):
        UString.math_list.show_bs(None, mode)

    def tab_change(e):
        MainPage.s_index = e.control.selected_index

    input_ui = Column(
        controls=[
            Container(
                Column(
                    [
                        equals,
                        Row(
                            controls=[
                                PopupMenuButton(
                                    icon=icons.ADD,
                                    tooltip="新建",
                                    items=[
                                        PopupMenuItem(
                                            icon=icons.FUNCTIONS,
                                            text="函数",
                                            on_click=lambda e: add(e, "fx")
                                        ),
                                        PopupMenuItem(
                                            icon=icons.EXPOSURE,
                                            text="方程",
                                            on_click=lambda e: add(e, "equ")
                                        )
                                    ]
                                )
                            ],
                            alignment=MainAxisAlignment.END
                        ),
                    ],
                    expand=True
                )
            )
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
                    Tabs(
                        selected_index=MainPage.s_index,
                        on_change=tab_change,
                        expand=1,
                        tabs=[
                            Tab(
                                text="函数",
                                content=input_ui
                            ),
                            Tab(
                                text="工具",
                                content=Text("Editing")
                            )
                        ]
                    )
                ],
                width=((_page.width - 100) / 7) * 1.8,
                alignment=MainAxisAlignment.START,

            ),
            VerticalDivider(width=1),
            Row(
                [
                    Container(
                        matplot_chart,
                        height=_page.height,
                    )
                ],
                width=((_page.width - 100) / 7) * 5.2,
                alignment=MainAxisAlignment.START
            )
        ], expand=True
    )
    ] if _page.width > 550 else [SafeArea(
        content=Column(
            [
                Column(
                    [
                        Container(
                            matplot_chart,
                            width=_page.width,
                            height=((_page.height - 150) / 7) * 4.5
                        ),
                    ]
                ),
                Divider(height=1),
                Column(
                    [
                        Tabs(
                            on_change=tab_change,
                            selected_index=MainPage.s_index,
                            expand=1,
                            tabs=[
                                Tab(
                                    text="函数",
                                    content=input_ui
                                ),
                                Tab(
                                    text="工具",
                                    content=Text("Editing")
                                )
                            ]
                        )
                    ]),
            ],
        )
    ), navbar]
    View(
        "/home",
        controls=content
    )
    return content
