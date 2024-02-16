import sympy
from flet import *

from matplot.latex.latex import latex_ui


# 展开函数
class Expand:
    def __init__(self, bs, page):
        self.solve_img = None
        self.max_height = None
        self.result = None
        self.value = None
        self.ui = None
        self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.input = TextField(label="多项式")

    def expand_ui(self):
        return [
            Text("展开多项式"),
            self.input
        ]

    def onclick(self, element, lists, running_class):
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        self.result = sympy.expand(equ)
        r_latex = sympy.latex(self.result)
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
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        r_latex = sympy.latex(self.result)
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


class Factor:
    def __init__(self, bs, page):
        self.solve_img = None
        self.max_height = None
        self.result = None
        self.value = None
        self.ui = None
        self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.input = TextField(label="多项式")

    def expand_ui(self):
        return [
            Text("因式分解"),
            self.input
        ]

    def onclick(self, element, lists, running_class):
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        self.result = sympy.factor(equ)
        r_latex = sympy.latex(self.result)
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
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        r_latex = sympy.latex(self.result)
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


class Collect:
    def __init__(self, bs, page):
        self.solve_img = None
        self.max_height = None
        self.result = None
        self.value = None
        self.ui = None
        self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.input = TextField(label="多项式")
        self.input_s = TextField(label="合并参数", width=100)

    def expand_ui(self):
        return [
            Text("合并同类项"),
            self.input_s,
            self.input
        ]

    def onclick(self, element, lists, running_class):
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        syms = sympy.symbols(self.input_s.value)
        self.result = sympy.collect(equ, syms)
        r_latex = sympy.latex(self.result)
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
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        r_latex = sympy.latex(self.result)
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


class Cancel:
    def __init__(self, bs, page):
        self.solve_img = None
        self.max_height = None
        self.result = None
        self.value = None
        self.ui = None
        self.latex_image = None
        self.equation = ""
        self._page = page
        self.bs = bs
        self.input = TextField(label="多项式")

    def expand_ui(self):
        return [
            Text("有理分式化简"),
            self.input
        ]

    def onclick(self, element, lists, running_class):
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        self.result = sympy.cancel(equ)
        r_latex = sympy.latex(self.result)
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
        self.value = self.input.value
        equ = sympy.sympify(self.value)
        self.latex_image = latex_ui(self._page, sympy.latex(equ))
        r_latex = sympy.latex(self.result)
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
