from copy import copy

from flet import *
import sympy

from basic.app_str import UString
from matplot.latex.latex import latex_ui, Latex


def warning(_page, tip: str):
    page.dialog = AlertDialog(
        modal=False,
        title=Text("错误"),
        content=Text(tip),
        open=True
    )
    _page.update()


class XCall:
    def __init__(self, bs, page):
        self.args = None
        self.solve_img = None
        self.max_height = None
        self.result = None
        self.value = None
        self.ui = None
        self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.input_y = TextField(label="Y值", width=130)
        self.f_name = TextField(label="函数名称", width=130)

    def xcall_ui(self):
        return [
            Text("根据Y求X"),
            self.f_name,
            self.input_y
        ]

    def onclick(self, element, lists, running_class):
        function_name = self.f_name.value
        try:
            y_value = sympy.sympify(self.input_y.value)
        except Exception:
            warning(self._page, "请输入数字")
            raise KeyError
        find = False
        for i in UString.lists:
            if i["mode"] == "fx" and i["name"] == function_name:
                find = True
                equ = sympy.sympify(i["text"])
                self.args = i["args"]
                try:
                    self.result = sympy.solve(sympy.Eq(equ, y_value))
                except Exception as e:
                    warning(self._page, str(e))
                    raise KeyError
        if not find:
            warning(self._page, "未找见函数名称")
            raise KeyError
        self.latex_image = Latex("return " + str(y_value), self.f_name.value, self.args, self._page).output_svg()
        r_latex = ""
        for i in self.result:
            r_latex += "x={},".format(str(sympy.latex(sympy.sympify(i))))
        self.solve_img = latex_ui(self._page, r_latex)[0]
        self.max_height = latex_ui(self._page, r_latex)[1]
        self.create_ui(element, lists, running_class)
        return self.ui

    def delete(self, element, lists, running_class):
        lists.remove(self.ui)
        running_class.remove(self)
        element.controls.remove(self.ui)
        self._page.update()

    def update_ui(self, element, lists, running_class):
        y_value = sympy.sympify(self.input_y.value)
        self.latex_image = Latex("return " + str(y_value), self.f_name.value, self.args, self._page).output_svg()
        r_latex = ""
        for i in self.result:
            r_latex += "x={},".format(str(sympy.latex(sympy.sympify(i))))
        self.solve_img = latex_ui(self._page, r_latex)[0]
        self.max_height = latex_ui(self._page, r_latex)[1]
        self.create_ui(element, lists, running_class)
        return self.ui

    def create_ui(self, element, lists, running_class):
        self.ui = Row(
            [
                Stack([
                    Column(
                        [
                            Row([
                                Text("函数".format(self.f_name.value, self.args)),
                                Container(
                                    content=self.latex_image[0],
                                    height=self.latex_image[1],
                                )
                            ], scroll=ScrollMode.AUTO,
                                width=(((self._page.width - 100) / 7) * 1.8 - 35) if self._page.width > 550 else (
                                        self._page.width - 55),

                            ), Row(
                            [
                                Icon(icons.SUBDIRECTORY_ARROW_RIGHT),
                                Container(
                                    content=Row(
                                        [self.solve_img]
                                    ),
                                    height=self.max_height,
                                )
                            ], scroll=ScrollMode.AUTO,
                            width=(((self._page.width - 100) / 7) * 1.8 - 35) if self._page.width > 550 else (
                                    self._page.width - 55)
                        )
                        ], top=5
                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="删除",
                                on_click=lambda e: self.delete(element, lists, running_class)
                            )
                        ]

                        ), right=0 if self._page.width > 550 else 20,

                    )
                ], width=(((self._page.width - 100) / 7) * 1.8) if self._page.width > 550 else self._page.width,
                )
            ],
            height=(self.latex_image[1] + self.max_height) + 45
        )


class YCall:
    def __init__(self, bs, page):
        self.args = None
        self.result = None
        self.value = None
        self.ui = None
        self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.input_x = TextField(label="X值", width=130)
        self.f_name = TextField(label="函数名称", width=130)

    def ycall_ui(self):
        return [
            Text("根据X求Y"),
            self.f_name,
            self.input_x
        ]

    def onclick(self, element, lists, running_class):
        function_name = self.f_name.value
        try:
            x_value = sympy.sympify(self.input_x.value)
        except Exception:
            warning(self._page, "请输入数字")
            raise KeyError
        find = False
        for i in UString.lists:
            if i["mode"] == "fx" and i["name"] == function_name:
                find = True
                equ = sympy.sympify(i["text"])
                self.args = i["args"]
                try:
                    self.result = equ.subs(sympy.symbols(self.args), x_value)
                except Exception as e:
                    warning(self._page, str(e))
                    raise KeyError
        if not find:
            warning(self._page, "未找见函数名称")
            raise KeyError
        self.latex_image = latex_ui(self._page, r"{}({}) = {}".format(function_name, sympy.latex(x_value),
                                                                      sympy.latex(self.result)))
        self.create_ui(element, lists, running_class)
        return self.ui

    def delete(self, element, lists, running_class):
        lists.remove(self.ui)
        running_class.remove(self)
        element.controls.remove(self.ui)
        self._page.update()

    def update_ui(self, element, lists, running_class):
        function_name = self.f_name.value
        x_value = sympy.sympify(self.input_x.value)
        self.latex_image = latex_ui(self._page, r"{}({}) = {}".format(function_name, sympy.latex(x_value),
                                                                      sympy.latex(self.result)))
        self.create_ui(element, lists, running_class)
        return self.ui

    def create_ui(self, element, lists, running_class):
        self.ui = Row(
            [
                Stack([
                    Column(
                        [
                            Row([
                                Text("函数".format(self.f_name.value, self.args)),
                                Container(
                                    content=self.latex_image[0],
                                    height=self.latex_image[1],
                                )
                            ], scroll=ScrollMode.AUTO,
                                width=(((self._page.width - 100) / 7) * 1.8 - 35) if self._page.width > 550 else (
                                        self._page.width - 55),

                            )
                        ], top=5
                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="删除",
                                on_click=lambda e: self.delete(element, lists, running_class)
                            )
                        ]

                        ), right=0 if self._page.width > 550 else 20,

                    )
                ], width=(((self._page.width - 100) / 7) * 1.8) if self._page.width > 550 else self._page.width,
                )
            ],
            height=(self.latex_image[1]) + 45
        )


class Intersection:
    def __init__(self, bs, page):
        self.equ_1 = self.equ_2 = self.args_1 = self.args_2 = self.latex_image_2 = self.args = self.solve_img = self.max_height = None
        self.result = []
        self.value = self.ui = self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.f_name_1 = TextField(label="函数名称1", width=130)
        self.f_name_2 = TextField(label="函数名称2", width=130)

    def intersection_ui(self):
        return [
            Text("求交点"),
            self.f_name_1,
            self.f_name_2
        ]

    def onclick(self, element, lists, running_class):
        function_1 = self.f_name_1.value
        function_2 = self.f_name_2.value
        equ_1 = equ_2 = 0
        find = [False] * 2
        for i in UString.lists:
            if i["mode"] == "fx" and i["name"] == function_1:
                find[0] = True
                equ_1 = sympy.sympify(i["text"]).subs(sympy.symbols(i["args"]), sympy.symbols("x"))
                self.args_1 = i["args"]
        for i in UString.lists:
            if i["mode"] == "fx" and i["name"] == function_2:
                find[1] = True
                equ_2 = sympy.sympify(i["text"]).subs(sympy.symbols(i["args"]), sympy.symbols("x"))
                self.args_2 = i["args"]
        if not all(find):
            warning(self._page, "未找见函数名称")
            raise KeyError
        result_x = sympy.solve(sympy.Eq(equ_1, equ_2))
        for i in result_x:
            self.result.append([i, equ_1.subs(sympy.symbols("x"), i)])
        self.latex_image = Latex("return " + str(equ_1), str(function_1), self.args_1, self._page).output_svg()
        self.latex_image_2 = Latex("return " + str(equ_2), str(function_2), self.args_2, self._page).output_svg()
        self.equ_1, self.equ_2 = equ_1, equ_2
        r_latex = ""
        for i in self.result:
            r_latex += "({},{})".format(sympy.latex(i[0]), sympy.latex(i[1]))
        self.solve_img = latex_ui(self._page, r_latex)[0]
        self.max_height = latex_ui(self._page, r_latex)[1]
        self.create_ui(element, lists, running_class)
        return self.ui

    def delete(self, element, lists, running_class):
        lists.remove(self.ui)
        running_class.remove(self)
        element.controls.remove(self.ui)
        self._page.update()

    def update_ui(self, element, lists, running_class):
        function_1 = self.f_name_1.value
        function_2 = self.f_name_2.value
        self.latex_image = Latex("return " + str(self.equ_1), str(function_1), self.args, self._page).output_svg()
        self.latex_image_2 = Latex("return " + str(self.equ_2), str(function_2), self.args, self._page).output_svg()
        r_latex = ""
        for i in self.result:
            r_latex += "({},{})".format(sympy.latex(i[0]), sympy.latex(i[1]))
        self.solve_img = latex_ui(self._page, r_latex)[0]
        self.max_height = latex_ui(self._page, r_latex)[1]
        self.create_ui(element, lists, running_class)
        return self.ui

    def draw(self):
        print(self.result)
        for i in self.result:
            UString.math_list.textInputs["point"]["x"].value = str(i[0])
            UString.math_list.textInputs["point"]["y"].value = str(i[1])
            _value = list(set(UString.p_n) - set(UString.p_e))  # 取补集查看默认的能用的函数名称
            _p_n = copy(UString.p_n)
            if not _value:
                # 如果没有可用的函数名称了，就加上下表，扩展默认函数名称列表
                UString.p_t += 1
                for a in _p_n:
                    UString.p_n.append("{}_{}".format(a, UString.p_t))
                _value = list(set(UString.p_n) - set(UString.p_e))  # 扩展完后再更新一下
            UString.math_list.textInputs["point"]["name"].value = _value[0]
            UString.math_list.add_point(None)

    def create_ui(self, element, lists, running_class):
        self.ui = Row(
            [
                Stack([
                    Column(
                        [
                            Row([
                                Container(
                                    content=self.latex_image[0],
                                    height=self.latex_image[1],
                                ),
                                Container(
                                    content=self.latex_image_2[0],
                                    height=self.latex_image_2[1],
                                )
                            ], scroll=ScrollMode.AUTO,
                                width=(((self._page.width - 100) / 7) * 1.8 - 35) if self._page.width > 550 else (
                                        self._page.width - 55),

                            ), Row(
                            [
                                Icon(icons.SUBDIRECTORY_ARROW_RIGHT),
                                Container(
                                    content=Row(
                                        [self.solve_img]
                                    ),
                                    height=self.max_height,
                                )
                            ], scroll=ScrollMode.AUTO,
                            width=(((self._page.width - 100) / 7) * 1.8 - 35) if self._page.width > 550 else (
                                    self._page.width - 55)
                        )
                        ], top=5
                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="删除",
                                on_click=lambda e: self.delete(element, lists, running_class)
                            ),
                            PopupMenuItem(
                                text="为每个点注册",
                                on_click=lambda e: self.draw()
                            )
                        ]

                        ), right=0 if self._page.width > 550 else 20,

                    )
                ], width=(((self._page.width - 100) / 7) * 1.8) if self._page.width > 550 else self._page.width,
                )
            ],
            height=(self.latex_image[1] + self.max_height) + 45
        )
