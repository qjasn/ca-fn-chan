import uuid

from flet import *
from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np
from numpy import *
from sympy import sympify, lambdify

from matplot.function.define_user_function import exec_plain
from matplot.function.draw_user_function import DrawUserFunction
from matplot.latex.latex import latex_ui

from basic.app_str import UString


class FitPolyUi:
    def __init__(self, bs, page):
        self.uuid = uuid.uuid1()
        self.function = None
        self.plot = None
        self._popt = None
        self.function_text = None
        self.result_function = None
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
        self.checkbox = Checkbox(
                                    value=True,
                                    on_change=self.on_change,
                                    visible=False
                                )
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

    def onclick(self, element, lists, running_class):
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
            self.function_text = "ax + b"
            self.function = MathFunction.linear_function
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
            result_function = "a={},b={}".format(_popt[0], _popt[1])
            self.result_function = result_function
            self.solve_img = latex_ui(self._page, result_function)[0]
            self.max_height = latex_ui(self._page, result_function)[1]
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
            self._content = latex_ui(self._page, function_text)
            _popt = []
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
            if polynomial == "polynomial-num-polyfit":
                result = np.polyfit(x_l, y_l, int(degree))
                for i in result:
                    _popt.append(round(i, 10))
            if polynomial == "polynomial-sci-curve":
                result, _ = curve_fit(fx, x_l, y_l)
                for i in result:
                    _popt.append(round(i, 10))
            for i, v in enumerate(_popt):
                result_text += "{} = {},".format(character[i], v)
            self.function = fx
            self.function_text = function_text
            self.result_function = result_text
            self._content = latex_ui(self._page, "f(x) = {}".format(function_text))
            self.solve_img = latex_ui(self._page, result_text)[0]
            self.max_height = latex_ui(self._page, result_text)[1]
        elif options == "sine_function" or options == "cosine_function":
            if options.startswith("sine"):
                self.function_text = "a sin(b x + c) + d"
                self.function = MathFunction.sine_function
            else:
                self.function_text = "a cos(b x + c) + d"
                self.function = MathFunction.cosine_function
            if self._page.client_storage.get("fx.fourier").startswith("enable"):
                fs = np.fft.fftfreq(len(x_l), x_l[1] - x_l[0])
                abs_y = abs(np.fft.fft(y_l))
                freq = abs(fs[np.argmax(abs_y[1:]) + 1])
                a0 = max(y_l) - min(y_l)
                a1 = 2 * pi * freq
                a2 = 0
                a3 = np.mean(y_l)
                p0 = [a0, a1, a2, a3]
                if options.startswith("sine"):
                    _popt, _ = curve_fit(MathFunction.sine_function, x_l, y_l, p0=p0)
                else:
                    _popt, _ = curve_fit(MathFunction.cosine_function, x_l, y_l, p0=p0)
                self.result_function = "a = {}, b = {}, c = {}, d = {}".format(_popt[0], _popt[1], _popt[2], _popt[3])
            else:
                if options.startswith("sine"):
                    _popt, _ = curve_fit(MathFunction.sine_function, x_l, y_l)
                else:
                    _popt, _ = curve_fit(MathFunction.cosine_function, x_l, y_l)

                self.result_function = "a = {}, b = {}, c = {}, d = {}".format(_popt[0], _popt[1], _popt[2], _popt[3])
            function_text = self.function_text
            result_text = self.result_function
            self._content = latex_ui(self._page, "f(x) = {}".format(function_text))
            self.solve_img = latex_ui(self._page, result_text)[0]
            self.max_height = latex_ui(self._page, result_text)[1]
        elif options == "tangent_function":
            _popt, _ = curve_fit(MathFunction.tangent_function, x_l, y_l)
            self.result_function = "a = {}, b = {}, c = {}, d = {}".format(_popt[0], _popt[1], _popt[2], _popt[3])
            function_text = self.function_text
            result_text = self.result_function
            self._content = latex_ui(self._page, "f(x) = {}".format(function_text))
            self.solve_img = latex_ui(self._page, result_text)[0]
            self.max_height = latex_ui(self._page, result_text)[1]
        elif options == "hook_function":
            _popt, _ = curve_fit(MathFunction.hook_function, x_l, y_l)
            self.result_function = "a = {}, b = {}".format(_popt[0], _popt[1])
            function_text = self.function_text
            result_text = self.result_function
            self._content = latex_ui(self._page, "f(x) = {}".format(function_text))
            self.solve_img = latex_ui(self._page, result_text)[0]
            self.max_height = latex_ui(self._page, result_text)[1]
        self._popt = _popt
        self.create_ui(element, lists, running_class)
        return self.return_ui

    def draw(self):
        ax = UString.matplot_chart.return_ax()
        if self._page.width > 550:
            _width = UString.width
            _width = ((_width - 100) / 7) * 5.2
            __width = _width - 50
            _height = UString.height
        else:
            _width = self._page.width
            __width = self._page.width
            _height = ((self._page.height - 150) / 7) * 4.5
        x1, x2, y1, y2 = -(_width / UString.step) / 2, (_width / UString.step) / 2, -(_height / UString.step) / 2, (
                _height / UString.step) / 2
        x = np.linspace(int(x1) - 1, int(x2) + 1, int(_width))
        y = [self.function(a, *self._popt) for a in x]
        content = {
            "x": x,
            "y": y
        }
        UString.draw_class.update({self.uuid: DrawUserFunction(content, self._page, "list")})
        UString.draw_class[self.uuid].draw()  # 绘制新函数的图像
        UString.matplot_chart.update_draw()  # 更新图像
        self.checkbox.visible = True
        self._page.update()

    def on_change(self,e):
        UString.draw_class[self.uuid].visible(e.control.value)  # 清除函数图像
        UString.matplot_chart.update_draw()  # 更新图像
        self._page.update()

    def create_ui(self, element, lists, running_class):
        self.return_ui = Row(
            [
                Stack([
                    Column(
                        [
                            Row([
                                self.checkbox,
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
                                on_click=lambda e: self.delete(element, lists, running_class)
                            ),
                            PopupMenuItem(
                                text="绘制",
                                on_click=lambda e: self.draw()
                            )
                        ]

                        ), right=0 if self._page.width > 550 else 20,

                    )
                ], width=(((self._page.width - 100) / 7) * 1.8) if self._page.width > 550 else self._page.width,
                )
            ],
            height=(self._content[1] + self.max_height) + 45
        )

    def delete(self, element, lists, running_class):
        if self.uuid in UString.draw_class.keys():
            UString.draw_class[self.uuid].delete()  # 清除函数图像
            UString.draw_class.pop(self.uuid)
            UString.matplot_chart.update_draw()  # 更新图像
        element.controls.remove(self.return_ui)
        lists.remove(self.return_ui)
        running_class.remove(self)
        self._page.update()

    def update_ui(self, element, lists, running_class):
        function_text = self.function_text
        result_text = self.result_function
        self._content = latex_ui(self._page, "f(x) = {}".format(function_text))
        self.solve_img = latex_ui(self._page, result_text)[0]
        self.max_height = latex_ui(self._page, result_text)[1]
        self.create_ui(element, lists, running_class)
        return self.return_ui


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
