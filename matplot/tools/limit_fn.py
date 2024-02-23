from copy import copy

import sympy
from flet import *
from scipy.optimize import fmin

from basic.app_str import UString
from matplot.latex.latex import Latex, latex_ui
from matplot.tools.calc_function import warning


class Limit:
    def __init__(self, bs, page: Page):
        self.equ = self.args = self.latex_image_2 = self.args = self.solve_img = self.max_height = None
        self.result = []
        self.value = self.ui = self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.f_name = TextField(label="函数名称", width=150)
        self.method = Dropdown(
            options=[
                dropdown.Option(key="max", text="最大值"),
                dropdown.Option(key="min", text="最小值")
            ],
            value="max",
            width=130
        )
        self.x0_input = TextField(label="初始迭代值", width=150)

    async def limit_ui(self):
        storage = await self._page.client_storage.get_async("fx.limit")
        if storage.startswith("sci"):
            ui = [
                Text("求极值"),
                self.method,
                self.f_name,
                self.x0_input
            ]
        else:
            ui = [
                Text("求极值"),
                self.method,
                self.f_name,
            ]
        return ui

    async def onclick(self, element, lists, running_class):
        function = self.f_name.value
        equ = 0
        find = False
        x1, x2, x3, x4 = sympy.symbols('x1,x2,x3,x4')
        for i in UString.lists:
            if i["mode"] == "fx" and i["name"] == function:
                find = True
                equ = sympy.sympify(i["text"]).subs(sympy.symbols(i["args"]), sympy.symbols("x"))
                self.args = i["args"]
        if not find:
            await warning(self._page, "未找见函数名称")
            raise KeyError
        storage = await self._page.client_storage.get_async("fx.limit")
        if storage.startswith("sci"):
            if self.method.value == "max":
                result_y = fmin(-sympy.lambdify(sympy.symbols("x"), equ), x0=float(self.x0_input.value))
            else:
                result_y = fmin(sympy.lambdify(sympy.symbols("x"), equ), x0=float(self.x0_input.value))
        else:
            result_y = []
            fn = sympy.lambdify(sympy.symbols("x"), equ)
            x2 = sympy.diff(fn(x1), x1)  # 求一阶导
            bb = sympy.solve(x2, x1)
            x3 = sympy.diff(fn(x1), x1, 2)  # 求二阶导
            condition = self.method.value == "max"
            for i in bb:
                if not condition and x3.subs(x1, i) > 0:
                    result_y.append(fn(x1).subs(x1, i))
                if condition and x3.subs(x1, i) < 0:
                    result_y.append(fn(x1).subs(x1, i))
        for l in result_y:
            for i in sympy.solve(sympy.Eq(equ, l)):
                self.result.append([i, l])

        self.latex_image = Latex("return " + str(equ), str(function), self.args, self._page).output_svg()
        self.equ = equ
        r_latex = ""
        if not self.result:
            r_latex = "No Solution"
        for i in self.result:
            r_latex += "({},{})".format(sympy.latex(i[0]), sympy.latex(i[1]))
        self.solve_img = latex_ui(self._page, r_latex)[0]
        self.max_height = latex_ui(self._page, r_latex)[1]
        self.create_ui(element, lists, running_class)
        return self.ui

    async def delete(self, e):
        element, lists, running_class = e.control.data
        lists.remove(self.ui)
        running_class.remove(self)
        element.controls.remove(self.ui)
        await self._page.update_async()

    def update_ui(self, element, lists, running_class):
        function = self.f_name.value
        self.latex_image = Latex("return " + str(self.equ), str(function), self.args, self._page).output_svg()
        r_latex = ""
        for i in self.result:
            r_latex += "({},{})".format(sympy.latex(i[0]), sympy.latex(i[1]))
        self.solve_img = latex_ui(self._page, r_latex)[0]
        self.max_height = latex_ui(self._page, r_latex)[1]
        self.create_ui(element, lists, running_class)
        return self.ui

    async def draw(self, e):
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
            await UString.math_list.add_point(None)

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
                                on_click=self.delete,
                                data=[element, lists, running_class]),
                            PopupMenuItem(
                                text="为每个点注册",
                                on_click=self.draw
                            )
                        ]

                        ), right=0 if self._page.width > 550 else 20,

                    )
                ], width=(((self._page.width - 100) / 7) * 1.8) if self._page.width > 550 else self._page.width,
                )
            ],
            height=(self.latex_image[1] + self.max_height) + 45
        )
