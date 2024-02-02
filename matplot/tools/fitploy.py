from flet import *


class FitPolyUi:
    def __init__(self, bs):
        self.option = None
        self.bs = bs
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

    def fit_poly_ui(self):
        self.option = Dropdown(
            options=[
                dropdown.Option("linear_function", "一次函数"),
                dropdown.Option("quadratic_function", "二次函数"),
                dropdown.Option("Sine function", "正弦函数"),
                dropdown.Option("cosine_function", "余弦函数"),
                dropdown.Option("tangent_function", "正切函数"),
                dropdown.Option("hook_function", "对勾函数"),
                dropdown.Option("custom_function", "自定义函数")
            ],
            value="linear_function",
            on_change=self.fit_ploy_input_ui,
            width=150
        )
        ui = [
            Text("拟合曲线"),
            self.option,
            self.input_ui
        ]
        return ui
