from copy import copy

import numpy as np

from basic.app_str import UString
from matplot.basic_graphic import MatPlotUi
from flet import *

from matplot.define_user_function import DefineUserFunction
from matplot.draw_user_function import DrawUserFunction
from ui.equation import EquationUI


class MainPage:

    def __init__(self, page, element):
        UString.matplot_chart = MatPlotUi(page)
        self.lists = UString.lists
        self.page = page
        self.ui = Column(controls=[], scroll=ScrollMode.ALWAYS,
                         height=(page.height - 70) if page.width > 550 else ((page.height - 150) / 7) * 2.5 - 20) # 渲染框大小
        self.name = TextField(label="名称", width=70) # 定义函数名称输入框
        self.args = TextField(label="参数", value="x", width=70) # 定义函数参数输入框
        self.text = TextField(label="函数内容", value="x") # 定义函数内容输入框
        self.equals = element # latex显示UI的引用
        # 函数输入模态框UI构建
        self.bs = BottomSheet(
            Container(
                Column([
                    Text("请输入数学公式", style=TextThemeStyle.BODY_MEDIUM),
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
                            TextButton("确认", on_click=self.add),
                            TextButton("取消", on_click=self.close_bs)
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
        _value = list(set(UString.f_n) - set(UString.a_e)) # 取补集查看默认的能用的函数名称
        _f_n = copy(UString.f_n)
        if not _value:
            #如果没有可用的函数名称了，就加上下表，扩展默认函数名称列表
            UString.t += 1
            for a in _f_n:
                print(_f_n)
                UString.f_n.append("{}_{}".format(a, UString.t))
            _value = list(set(UString.f_n) - set(UString.a_e)) # 扩展完后再更新一下
        print(UString.f_n)
        self.name = TextField(label="Name", value=_value[0], width=70)
        self.bs.content.content.controls[2].controls[0].content.controls[1].content.controls = [self.name, Text("("),
                                                                                                self.args, Text(") ="),
                                                                                                self.text] # 这一段是不是很震惊，那么我要告诉你了，这是我写的最失败的一段代码，根本不具有任何可维护性与扩展性，后面有时间了会改掉
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
        # 判断输入是否为空
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("错误"),
                content=Text("任何一个输入值都不能为空"),
                open=True
            )
            self.page.update()
        elif self.name.value in UString.a_e:
            # 判断函数名称是否存在
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("错误"),
                content=Text("函数名称已经存在"),
                open=True
            )
            self.page.update()
        else:
            # 将输入的值结构化，具体规范见app_str.py
            content = {
                "name": self.name.value,
                "args": self.args.value,
                "text": self.text.value
            }
            # 将这个结构化的函数加入全局变量方便其它函数与Class访问
            UString.lists.append(content)
            UString.a_e.append(self.name.value)
            DrawUserFunction(content, self.page).draw(UString.matplot_chart.return_ax()) # 绘制新函数的图像
            UString.matplot_chart.update_draw() # 更新图像
        self.close_bs(None)
        self.equals.content = self.create_ui()
        self.page.update()

    def matplot_ui(self):
        # 从全局变量中构建函数图像的UI，该方法在初始化/页面分辨率改变时会触发
        print(UString.lists)
        for content in UString.lists:
            DrawUserFunction(content, self.page).draw(UString.matplot_chart.return_ax())
            UString.matplot_chart.update_draw()
        return UString.matplot_chart.update_draw()

    def create_ui(self):
        # 构建函数显示UI
        if not self.lists:
            self.ui.controls = [Text("请点击右下角的加号新建数学公式")]
        else:
            self.ui.controls = []
            # 渲染存在的latex公式
        for i in self.lists:
            print("return {}".format(i["text"]))
            self.ui.controls.append(
                EquationUI(name=i["name"], args=i["args"], text="return {}".format(i["text"]),
                           page=self.page, subscript=True).create_ui(i, self.equals))
        return self.ui


def main_page(_page, navbar):
    print(UString.width)
    equals = Container() # latex公式
    _control = MainPage(_page, equals)
    equals.content = _control.create_ui()
    UString.matplot_chart.draw()
    matplot_chart = _control.matplot_ui() # 函数图像UI

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
