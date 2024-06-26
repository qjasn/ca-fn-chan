from flet import *

from basic.app_str import UString
from basic.tiny_fn import alert
from matplot.tools.calc_function import warning


async def settings_page(_page: Page, navbar):
    async def dark_mode_change(e):
        # 单选更新后触发
        _mode = await _page.client_storage.get_async("fx.darkMode")
        await _page.client_storage.set_async("fx.darkMode", e.control.value)
        _page.theme_mode = UString.darkMode[e.control.value]
        UString.change_dark = True
        await _page.update_async()

    async def polyfit_liner_update(e):
        _mode = await _page.client_storage.get_async("fx.liner")
        await _page.client_storage.set_async("fx.liner", e.control.value)

    async def polyfit_polynomial_update(e):
        _mode = await _page.client_storage.get_async("fx.polynomial")
        await _page.client_storage.set_async("fx.polynomial", e.control.value)

    async def fourier_update(e):
        _mode = await _page.client_storage.get_async("fx.fourier")
        await _page.client_storage.set_async("fx.fourier", e.control.value)

    async def limit_update(e):
        _mode = await _page.client_storage.get_async("fx.limit")
        await _page.client_storage.set_async("fx.limit", e.control.value)

    async def refresh(e):
        await _page.client_storage.set_async("fx.darkMode", "SYSTEM")
        await _page.client_storage.set_async("fx.liner", "liner-sci-liner")
        await _page.client_storage.set_async("fx.polynomial", "polynomial-num-polyfit")
        await _page.client_storage.set_async("fx.fourier", "enable-fourier")
        await _page.client_storage.set_async("fx.limit", "sym-derivative")
        _page.theme_mode = UString.darkMode["SYSTEM"]
        UString.change_dark = True
        await _page.update_async()
        await alert(_page,"提示", "更改已应用,重新切入该页面即可查看")

    async def start_again(e):
        await _page.client_storage.remove_async("fx.start")
        await alert(_page, "提示", "更改已应用,重新进入应用查看更改")

    dark_mode_ui = RadioGroup(Column([
        Radio(value="SYSTEM", label="跟随系统"),
        Radio(value="LIGHT", label="明亮"),
        Radio(value="DARK", label="暗黑")

    ], alignment=MainAxisAlignment.START),
        value=await _page.client_storage.get_async("fx.darkMode"),
        on_change=dark_mode_change
    )
    liner_fn_set = Dropdown(
        options=[
            dropdown.Option(key="liner-num-polyfit", text="(NUMPY)最小二乘法拟合"),
            dropdown.Option(key="liner-sci-liner", text="(SCIPY)线性回归拟合[默认]"),
            dropdown.Option(key="liner-sci-curve", text="(SCIPY)高斯回归拟合")
        ],
        value=await _page.client_storage.get_async("fx.liner"),
        on_change=polyfit_liner_update
    )
    polynomial_fn_set = Dropdown(
        options=[
            dropdown.Option("polynomial-num-polyfit", text="(NUMPY)最小二乘法拟合[默认]"),
            dropdown.Option("polynomial-sci-curve", text="(SCIPY)高斯回归拟合")
        ],
        value=await _page.client_storage.get_async("fx.polynomial"),
        on_change=polyfit_polynomial_update
    )
    fourier_transform_set = Dropdown(
        options=[
            dropdown.Option("enable-fourier", text="启用[默认]"),
            dropdown.Option("disable-fourier", text="关闭")
        ],
        value=await _page.client_storage.get_async("fx.fourier"),
        on_change=fourier_update
    )
    the_limit_set = Dropdown(
        options=[
            dropdown.Option("sci-simplex", text="(SCIPY)下降单纯法"),
            dropdown.Option("sym-derivative", text="(SYMPY)二阶导求极值[默认]")
        ],
        value=await _page.client_storage.get_async("fx.limit"),
        on_change=limit_update
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
                ),
                Row(
                    [
                        Text("求极值方法:"),
                        the_limit_set
                    ]
                ),
                Divider(height=1),
                ListTile(title=Text("其它")),
                Divider(height=1),
                Row(
                    [
                        ElevatedButton("还原所有设置",on_click=refresh),
                        ElevatedButton("重新启动引导界面", on_click=start_again)
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
