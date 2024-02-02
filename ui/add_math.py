from copy import copy

from flet import *

from basic.app_str import UString
from matplot.draw_user_function import DrawUserFunction
from ui.equation_ui import EquationUI
from ui.function_ui import FunctionUI
from ui.point_ui import PointUI


class AddMath:
    def __init__(self, page: Page, element):
        self.lists = UString.lists
        self.page = page
        self.ui = Column(controls=[], scroll=ScrollMode.ALWAYS,
                         height=(page.height - 120) if page.width > 550 else ((
                                                                                      page.height - 150) / 7) * 2.5 - 70)  # 渲染框大小
        self.textInputs = {
            "fx": {
                "name": TextField(label="名称", width=70),  # 定义函数名称输入框
                "args": TextField(label="参数", value="x", width=70),  # 定义函数参数输入框
                "text": TextField(label="函数内容", value="x")  # 定义函数内容输入框
            },
            "equ": {
                "equ": TextField(label="内容", value="x = 1"),
                "args": TextField(label="求解参数", width=100, value="x")
            },
            "point": {
                "x": TextField(label="x", value="1", width=100),
                "y": TextField(label="y", value="1", width=100),
                "name": TextField(label="Name", value="1", width=200),
            }
        }
        self.equals = element  # latex显示UI的引用
        self.button = TextButton("确认", on_click=self.add_function)  # 模态框输入按钮
        self.input = Row(scroll=ScrollMode.ALWAYS)  # 模态框显示UI
        # 函数输入模态框UI构建
        self.bs = BottomSheet(
            Container(
                Column([
                    Text("请输入数学公式", theme_style=TextThemeStyle.BODY_MEDIUM),
                    Divider(height=1),
                    Row(
                        scroll=ScrollMode.ALWAYS,
                        controls=[
                            Container(
                                padding=10,
                                content=Row([
                                    Container(
                                        self.input
                                    ), ]))
                        ],
                    ),
                    Row(
                        [
                            self.button,
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
        pass

    def show_bs(self, e, mode="fx"):
        if mode == "fx":
            self.button.on_click = self.add_function
            _value = list(set(UString.f_n) - set(UString.a_e))  # 取补集查看默认的能用的函数名称
            _f_n = copy(UString.f_n)
            if not _value:
                # 如果没有可用的函数名称了，就加上下表，扩展默认函数名称列表
                UString.t += 1
                for a in _f_n:
                    UString.f_n.append("{}_{}".format(a, UString.t))
                _value = list(set(UString.f_n) - set(UString.a_e))  # 扩展完后再更新一下
            self.textInputs["fx"]["name"] = TextField(label="Name", value=_value[0], width=70)
            self.input.controls = [self.textInputs["fx"]["name"], Text("("),
                                   self.textInputs["fx"]["args"], Text(") ="),
                                   self.textInputs["fx"]["text"]]
        elif mode == "equ":
            self.button.on_click = self.add_equation
            self.input.controls = [self.textInputs["equ"]["equ"], self.textInputs["equ"]["args"]]
        elif mode == "point":
            self.button.on_click = self.add_point
            _value = list(set(UString.p_n) - set(UString.p_e))  # 取补集查看默认的能用的函数名称
            _p_n = copy(UString.p_n)
            if not _value:
                # 如果没有可用的函数名称了，就加上下表，扩展默认函数名称列表
                UString.p_t += 1
                for a in _p_n:
                    UString.p_n.append("{}_{}".format(a, UString.p_t))
                _value = list(set(UString.p_n) - set(UString.p_e))  # 扩展完后再更新一下
            self.textInputs["point"]["name"].value = _value[0]
            self.input.controls = [self.textInputs["point"]["name"], Text("("),
                                   self.textInputs["point"]["x"], Text(","),
                                   self.textInputs["point"]["y"], Text(")")]

        self.page.update()
        self.bs.open = True
        self.bs.update()

    def add_point(self, e):
        x = self.textInputs["point"]["x"]
        y = self.textInputs["point"]["y"]
        name = self.textInputs["point"]["name"]
        if any([x.value == "", y.value == "", name.value == ""]):
            # 判断输入是否为空
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("错误"),
                content=Text("任何一个输入值都不能为空"),
                open=True
            )
        elif name.value in UString.p_e:
            # 判断函数名称是否存在
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("错误"),
                content=Text("函数名称已经存在"),
                open=True
            )
            self.page.update()
        else:
            content = {
                "x": x.value,
                "y": y.value,
                "name": name.value,
                "mode": "point"
            }
            UString.lists.append(content)
            UString.p_e.append(name.value)
            UString.draw_class.update({name.value: DrawUserFunction(content, self.page, "point")})
            UString.draw_class[name.value].draw()  # 绘制新函数的图像
            self.close_bs(None)
            UString.matplot_chart.update_draw()  # 更新图像
        self.close_bs(None)
        self.equals.content = self.create_ui()
        self.page.update()

    def add_equation(self, e):
        _equ = self.textInputs["equ"]["equ"]
        _args = self.textInputs["equ"]["args"]
        if any([_equ.value == "", _args.value == ""]):
            # 判断输入是否为空
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("错误"),
                content=Text("任何一个输入值都不能为空"),
                open=True
            )
        else:
            content = {
                "equ": _equ.value,
                "args": _args.value,
                "mode": "equ"
            }
            UString.lists.append(content)
            self.close_bs(None)
            self.equals.content = self.create_ui()
            self.page.update()

    def close_bs(self, e):
        self.bs.open = False
        self.bs.update()

    def add_function(self, e):
        _text = self.textInputs["fx"]
        if any([
            _text["name"].value == "",
            _text["args"].value == "",
            _text["text"].value == "",
        ]):
            # 判断输入是否为空
            self.page.dialog = AlertDialog(
                modal=False,
                title=Text("错误"),
                content=Text("任何一个输入值都不能为空"),
                open=True
            )
            self.page.update()
        elif _text["name"].value in UString.a_e:
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
                "mode": "fx",
                "name": _text["name"].value,
                "args": _text["args"].value,
                "text": _text["text"].value,
            }
            # 将这个结构化的函数加入全局变量方便其它函数与Class访问
            UString.lists.append(content)
            UString.a_e.append(_text["name"].value)
            UString.draw_class.update({_text["name"].value: DrawUserFunction(content, self.page)})
            UString.draw_class[_text["name"].value].draw()  # 绘制新函数的图像
            UString.matplot_chart.update_draw()  # 更新图像
        self.close_bs(None)
        self.equals.content = self.create_ui()
        self.page.update()

    def create_ui(self):
        # 构建函数显示UI
        if not self.lists:
            self.ui.controls = [Text("请点击右下角的加号新建数学公式")]
        else:
            self.ui.controls = []
            # 渲染存在的latex公式
        for i in self.lists:
            if i["mode"] == "fx":
                self.ui.controls.append(
                    FunctionUI(name=i["name"], args=i["args"], text="return {}".format(i["text"]),
                               page=self.page, subscript=True, use_math_symbols=True).create_ui(i, self.equals))
            elif i["mode"] == "equ":
                self.ui.controls.append(
                    EquationUI(page=self.page, equ=i["equ"], args=i["args"]).create_ui(self.equals, i))
            elif i["mode"] == "point":
                self.ui.controls.append((
                    PointUI(page=self.page, name=i["name"], x=i["x"], y=i["y"]).create_ui(i, self.equals)
                ))
        return self.ui

    def nav_change(self):
        return self.ui
