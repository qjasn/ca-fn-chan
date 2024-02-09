from flet import *
from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np
from sympy import *

from matplot.function.define_user_function import exec_plain
from matplot.latex.latex import latex_ui

from basic.app_str import UString


class FitPolyUi:
    def __init__(self, bs, page):
        self._content = None
        self.max_height = None
        self.return_ui = None
        self.solve_img = None
        self.ui = None
        self.option = None
        self.bs = bs
        self._page = page
        liner = self._page.client_storage.get("fx.liner")
        polynomial = self._page.client_storage.get("fx.polynomial")
        self.points = TextField(label="点", width=200)
        self.degree_ui = TextField(label="最高次", width=100)
        if liner.startswith("liner-num") and polynomial.startswith("polynomial-num"):
            self.input_ui = Row(
                [
                    self.degree_ui,
                    self.points
                ]
            )
        else:
            self.input_ui = Row(
                [
                    self.points
                ]
            )

    def fit_ploy_input_ui(self, e):
        if e.control.value != "custom_function" and e.control.value != "polynomial_function":
            self.input_ui.controls = [
                self.points
            ]
        elif e.control.value == "polynomial_function":
            self.input_ui.controls = [
                self.degree_ui,
                self.points
            ]
        else:
            self.input_ui.controls = [
                self.points,
                TextField(label="求解参数", width=130),
                TextField(label="求解函数"),
            ]
        self.bs.update()

    def fit_poly_ui(self):
        options = []
        liner = self._page.client_storage.get("fx.liner")
        polynomial = self._page.client_storage.get("fx.polynomial")
        if liner.startswith("liner-num") and polynomial.startswith("polynomial-num"):
            options = [
                dropdown.Option("polynomial_function", "多项式函数")
            ]
        elif liner.startswith("liner-sci") and polynomial.startswith("polynomial-num"):
            options = [
                dropdown.Option("linear_function", "一次函数"),
                dropdown.Option("polynomial_function", "非线性多项式函数"),
            ]
        else:
            options = [
                dropdown.Option("linear_function", "一次函数"),
                dropdown.Option("polynomial_function", "非线性多项式函数"),
            ]
        options += [
            dropdown.Option("sine_function", "正弦函数"),
            dropdown.Option("cosine_function", "余弦函数"),
            dropdown.Option("tangent_function", "正切函数"),
            dropdown.Option("hook_function", "对勾函数"),
            # dropdown.Option("custom_function", "自定义函数")
        ]
        self.option = Dropdown(
            options=options,
            value="linear_function" if not liner.startswith("liner-num") or not polynomial.startswith("polynomial-num")
            else "polynomial_function",
            on_change=self.fit_ploy_input_ui,
            width=170
        )
        self.ui = [
            Text("拟合曲线"),
            self.option,
            self.input_ui
        ]
        return self.ui

    def warning(self, tip: str):
        self._page.dialog = AlertDialog(
            modal=False,
            title=Text("错误"),
            content=Text(tip),
            open=True
        )
        self._page.update()

    def onclick(self, element):
        points = self.points.value
        options = self.option.value
        liner = self._page.client_storage.get("fx.liner")
        polynomial = self._page.client_storage.get("fx.polynomial")
        for i in self.input_ui.controls:
            if i.value == "":
                self.warning("任何值均不能为空")
        x_l = []
        y_l = []
        # 点的数量与对应函数处理
        if options == "polynomial_function":
            if len(points.split(",")) < int(self.input_ui.controls[0].value):
                print(points)
                print(int(self.input_ui.controls[0].value))
                self.warning("函数最高次大于输入点的数量")
                raise KeyError
        elif options == "linear_function":
            if len(points.split(",")) < 2:
                self.warning("函数最高次大于输入点的数量")
                raise KeyError
        for i in points.split(","):
            for p in UString.lists:
                if all([p["name"] == i, p["mode"] == "point"]):
                    x_l.append(float(p["x"]))
                    y_l.append(float(p["y"]))
        _popt = []
        # 线性函数
        if options == "linear_function":
            self._content = latex_ui(self._page, "f(x) = ax + b")
            if liner == "liner-sci-liner":
                result = linregress(x_l, y_l)
                _popt = [result[0], result[1]]
            if liner == "liner-num-polyfit":
                result = np.polyfit(x_l, y_l, 1)
                result[0] = round(float(result[0]), 10)
                result[1] = round(float(result[1]), 10)
                _popt = result
            if liner == "liner-sci-curve":
                result, _ = curve_fit(MathFunction.linear_function, x_l, y_l)
                result[0] = round(float(result[0]), 10)
                result[1] = round(float(result[1]), 10)
                _popt = result
            self.solve_img = latex_ui(self._page, "a={},b={}".format(_popt[0], _popt[1]))[0]
            self.max_height = latex_ui(self._page, "a={},b={}".format(_popt[0], _popt[1]))[1]
        # 非线性多项式函数
        elif options == "polynomial_function":
            character = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
            degree = self.degree_ui.value
            function_text, result_text = "", ""
            try:
                _degree = int(degree)
            except ValueError:
                self.warning("请输入数字")
                raise KeyError
            if _degree < 1:
                self.warning("请输入不小于1的数字")
                raise KeyError
            if _degree > 10:
                self.warning("请输入不大于10的数字")
                raise KeyError
            for i, c in enumerate(character[:(_degree + 1)]):
                if _degree - i == 1:
                    function_text += r"{} x+".format(c)
                elif _degree - i == 0:
                    function_text += r"{}".format(c)
                else:
                    function_text += r"{} x^{}+".format(c, _degree - i)
            print(function_text)
            self._content = latex_ui(self._page, function_text)
            _popt = []
            if polynomial == "polynomial-num-polyfit":
                result = np.polyfit(x_l, y_l, int(degree))
                for i in result:
                    _popt.append(round(i, 10))
            if polynomial == "polynomial-sci-curve":
                args = "x,"
                for i in character[:(_degree + 1)]:
                    args += "{},".format(i)
                fx_text = ""
                for i, c in enumerate(character[:(_degree + 1)]):
                    if _degree - i == 1:
                        fx_text += r"{}*x+".format(c)
                    elif _degree - i == 0:
                        fx_text += r"{}".format(c)
                    else:
                        fx_text += r"{}*x**{}+".format(c, _degree - i)
                fx = exec_plain(args, fx_text)
                print(args, fx_text, x_l, y_l)
                result, _ = curve_fit(fx, x_l, y_l)
                for i in result:
                    _popt.append(round(i, 10))
            for i, v in enumerate(_popt):
                result_text += "{} = {} ".format(character[i], v)
            self._content = latex_ui(self._page, "f(x) = {}".format(function_text))
            self.solve_img = latex_ui(self._page, result_text)[0]
            self.max_height = latex_ui(self._page, result_text)[1]
        self.create_ui(element)
        return self.return_ui

    def create_ui(self, element):
        self.return_ui = Row(
            [
                Stack([
                    Column(
                        [
                            Row([
                                Container(
                                    content=self._content[0],
                                    height=self._content[1],
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
                                on_click=lambda e: self.delete(element)
                            )
                        ]

                        ), right=0 if self._page.width > 550 else 20,

                    )
                ], width=(((self._page.width - 100) / 7) * 1.8) if self._page.width > 550 else self._page.width,
                )
            ],
            height=(self._content[1] + self.max_height) + 45
        )

    def delete(self, element):
        element.controls.remove(self.return_ui)
        self._page.update()


class MathFunction:
    @staticmethod
    def linear_function(x, a, b):
        y = x * a + b
        return y

    @staticmethod
    def quadratic_function(x, a, b, c):
        y = a * (x ** 2) + b * x + c
        return y

    @staticmethod
    def sine_function(x, a, b, c, d):
        y = a * sin(b * x + c) + d
        return y

    @staticmethod
    def cosine_function(x, a, b, c, d):
        y = a * cos(b * x + c) + d
        return y

    @staticmethod
    def tangent_function(x, a, b, c, d):
        y = a * tan(b * x + c) + d
        return y

    @staticmethod
    def hook_function(x, a, b):
        y = a * x + b / x
        return y


class CustomFunction:
    def __init__(self, args, fx):
        self.args = args
        self.fx = fx
        self.map = {}
        for i in args.split(","):
            exec("result = symbols('{}')".format(i))
            self.map[i] = locals()["result"]
        _fx = ""
        for i in args.split(","):
            _fx = fx.replace(i, 'self.map["{}"]'.format(i))
        exec("result = ({})".format(args))
        self.set = locals()["result"]
        self.eq = sympify(_fx)
        self.fn = lambdify(self.set, self.eq)
