from flet import *
import sympy

from basic.app_str import UString
from matplot.latex.latex import latex_ui


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
        self.input_y = TextField(label="Y值", width=50)
        self.f_name = TextField(label="函数名称")

    def expand_ui(self):
        return [
            Text("有理分式化简"),
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
        self.latex_image = latex_ui(self._page, sympy.latex(sympy.sympify(y_value)))
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
        self.latex_image = latex_ui(self._page, sympy.latex(sympy.sympify(y_value)))
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
                                Text("函数 {}({})=".format(self.f_name.value,self.args)),
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
