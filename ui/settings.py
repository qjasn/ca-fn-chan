from flet import *

from basic.app_str import UString


def settings_page(_page, navbar):
    def dark_mode_change(e):
        # 单选更新后触发
        _mode = _page.client_storage.get("fx.darkMode")
        _page.client_storage.set("fx.darkMode", e.control.value)
        _page.theme_mode = UString.darkMode[e.control.value]
        UString.change_dark = True
        _page.update()

    def polyfit_liner_update(e):
        _mode = _page.client_storage.get("fx.liner")
        _page.client_storage.set("fx.liner", e.control.value)

    def polyfit_polynomial_update(e):
        _mode = _page.client_storage.get("fx.polynomial")
        _page.client_storage.set("fx.polynomial", e.control.value)

    def fourier_update(e):
        _mode = _page.client_storage.get("fx.fourier")
        _page.client_storage.set("fx.fourier", e.control.value)

    dark_mode_ui = RadioGroup(Column([
        Radio(value="SYSTEM", label="跟随系统"),
        Radio(value="LIGHT", label="明亮"),
        Radio(value="DARK", label="暗黑")

    ], alignment=MainAxisAlignment.START),
        value=_page.client_storage.get("fx.darkMode"),
        on_change=dark_mode_change
    )
    liner_fn_set = Dropdown(
        options=[
            dropdown.Option(key="liner-num-polyfit", text="(NUMPY)最小二乘法拟合"),
            dropdown.Option(key="liner-sci-liner", text="(SCIPY)线性回归拟合[默认]"),
            dropdown.Option(key="liner-sci-curve", text="(SCIPY)高斯回归拟合")
        ],
        value=_page.client_storage.get("fx.liner"),
        on_change=polyfit_liner_update
    )
    polynomial_fn_set = Dropdown(
        options=[
            dropdown.Option("polynomial-num-polyfit", text="(NUMPY)最小二乘法拟合[默认]"),
            dropdown.Option("polynomial-sci-curve", text="(SCIPY)高斯回归拟合")
        ],
        value=_page.client_storage.get("fx.polynomial"),
        on_change=polyfit_polynomial_update
    )
    fourier_transform_set = Dropdown(
        options=[
            dropdown.Option("enable-fourier", text="启用[默认]"),
            dropdown.Option("disable-fourier", text="关闭")
        ],
        value=_page.client_storage.get("fx.fourier"),
        on_change=fourier_update
    )
    content = Column(
        [
            Column([
                ListTile(title=Text("设置")),
                ListTile(leading=Icon(icons.DARK_MODE), title=Text("暗黑模式")),
                Divider(height=1),
                dark_mode_ui,
                Divider(height=1),
                ListTile(title=Text("数学设置")),
                Divider(height=1),
                ListTile(title=Text("拟合函数相关")),
                Row(
                    [
                        Text("一次函数拟合算法:"),
                        liner_fn_set
                    ],
                    scroll=ScrollMode.ALWAYS
                ),
                Row(
                    [
                        Text("非线性多项式拟合算法:"),
                        polynomial_fn_set
                    ],
                    scroll=ScrollMode.ALWAYS
                ),
                Row(
                    [
                        Text("正余弦函数傅立叶变换预处理:"),
                        fourier_transform_set
                    ]
                )
            ],
                alignment=MainAxisAlignment.START,
                scroll=ScrollMode.ALWAYS
            )],
        scroll=ScrollMode.ALWAYS,
        alignment=MainAxisAlignment.START,
        expand=True
    )

    return [Row([
        navbar, VerticalDivider(width=1), content
    ], expand=True)] if _page.width > 550 else [SafeArea(content), navbar]
