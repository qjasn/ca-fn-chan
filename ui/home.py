from copy import copy

from basic.app_str import UString
from matplot.basic_graphic import MatPlotUi
from flet import *

from ui.equation import EquationUI


class HomePage:

    def __init__(self, page, element):
        self.lists = UString.lists
        self.page = page
        self.ui = Column(controls=[], scroll=ScrollMode.ALWAYS,
                         height=(page.height - 70) if page.width > 550 else ((page.height - 150) / 7) * 2.5 - 20)
        self.name = TextField(label="Name", width=70)
        self.args = TextField(label="Args", value="x", width=70)
        self.text = TextField(label="Function", value="x")
        self.equals = element
        self.bs = BottomSheet(
            Container(
                Column([
                    Text("Enter the math equation", style=TextThemeStyle.BODY_MEDIUM),
                    Divider(height=1),
                    Row(
                        scroll=ScrollMode.ALWAYS,
                        controls=[
                            Container(
                                padding=10,
                                content=Row([Dropdown(
                                    options=[
                                        dropdown.Option("fn")
                                    ],
                                    width=100,
                                    value="fn"
                                ),
                                    Container(
                                        Row(
                                            [
                                                self.name,
                                                Text("("),
                                                self.args,
                                                Text(") ="),
                                                self.text
                                            ],
                                            scroll=ScrollMode.ALWAYS,

                                        )
                                    ), ]))
                        ],
                    ),
                    Row(
                        [
                            TextButton("Ok", on_click=self.add),
                            TextButton("Cancel", on_click=self.close_bs)
                        ]
                    )
                ],
                    tight=True),
                padding=10,
            ),
            on_dismiss=self.bs_dismissed,
        )
        page.overlay.append(self.bs)

    def bs_dismissed(self, e):
        print(e)
        print("Dismissed!")

    def show_bs(self, e):
        _value = list(set(UString.f_n) - set(UString.a_e))
        _f_n = copy(UString.f_n)
        if not _value:
            UString.t += 1
            for a in _f_n:
                print(_f_n)
                UString.f_n.append("{}_{}".format(a, UString.t))
        _value = list(set(UString.f_n) - set(UString.a_e))
        print(UString.f_n)
        self.name = TextField(label="Name", value=_value[0], width=70)
        self.bs.content.content.controls[2].controls[0].content.controls[1].content.controls = [self.name, Text("("),
                                                                                                self.args, Text(") ="),
                                                                                                self.text]
        self.page.update()
        self.bs.open = True
        self.bs.update()

    def close_bs(self, e):
        self.bs.open = False
        self.bs.update()

    def add(self, e):
        if any([
            self.name.value == "",
            self.args.value == "",
            self.text.value == "",
        ]):
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("Error"),
                content=Text("Value cannot be empty"),
                open=True
            )
            self.page.update()
        elif self.name.value in UString.a_e:
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("Error"),
                content=Text("Function name has already exist"),
                open=True
            )
            self.page.update()
        else:
            content = {
                "name": self.name.value,
                "args": self.args.value,
                "text": self.text.value
            }
            UString.lists.append(content)
            UString.a_e.append(self.name.value)
            print(self.lists)
        self.close_bs(None)
        self.equals.content = self.create_ui()
        self.page.update()

    def create_ui(self):
        if not self.lists:
            self.ui.controls = [Text("Enter the function")]
        else:
            self.ui.controls = []
        for i in self.lists:
            print("return {}".format(i["text"]))
            self.ui.controls.append(
                EquationUI(name=i["name"], args=i["args"], text="return {}".format(i["text"]),
                           page=self.page, subscript=True).create_ui(i, self.equals))
        return self.ui


def home_page(_page, navbar):
    print(UString.width)
    matplot_chart = MatPlotUi(_page).draw()

    equals = Container()
    _control = HomePage(_page, equals)
    equals.content = _control.create_ui()

    def add(e):
        _control.show_bs(None)

    input_ui = Column(
        controls=[
            Container(
                Column(
                    [
                        equals,
                        Row(
                            [
                                IconButton(
                                    icon=icons.ADD, on_click=add
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
                    input_ui
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
