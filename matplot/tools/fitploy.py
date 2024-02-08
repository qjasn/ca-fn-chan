from flet import *
from scipy.optimize import curve_fit
from scipy.stats import linregress
from sympy import *

from basic.app_str import UString


class FitPolyUi:
    def __init__(self, bs, page):
        self.ui = None
        self.option = None
        self.bs = bs
        self._page = page
        self.input_ui = Row(
            [
                TextField(label="点", width=200)
            ]
        )

    def fit_ploy_input_ui(self, e):
        print(e.control.value)
        if e.control.value != "custom_function":
            self.input_ui.controls = [
                TextField(label="点", width=200)
            ]
        else:
            self.input_ui.controls = [
                TextField(label="点", width=200),
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
                dropdown.Option("quadratic_function", "二次函数"),
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
            value="linear_function" if liner.startswith("liner-sci") else "polynomial_function",
            on_change=self.fit_ploy_input_ui,
            width=170
        )
        self.ui = [
            Text("拟合曲线"),
            self.option,
            self.input_ui
        ]
        return self.ui

    def onclick(self):
        points = self.input_ui.controls[0].value
        x_l = []
        y_l = []
        for i in points.split(","):
            for p in UString.lists:
                if all([p["name"] == i, p["mode"] == "point"]):
                    x_l.append(float(p["x"]))
                    y_l.append(float(p["y"]))
        print(x_l, y_l)
        _code = "popt, pocv = curve_fit(MathFunction.{},x_l,y_l)".format(self.option.value)
        print(_code, x_l, y_l)
        exec(_code)
        _popt = locals()["popt"]
        text = []
        for i in _popt:
            text.append(Text(i))
        return Container(
            Row(
                text
            )
        )


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
    def sine_function(x, a, b, c):
        y = a * sin(x + b) + c
        return y

    @staticmethod
    def cosine_function(x, a, b, c):
        y = a * cos(x + b) + c
        return y

    @staticmethod
    def tangent_function(x, a, b, c):
        y = a * tan(x + b) + c
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
