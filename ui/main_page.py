import asyncio

from flet import *
import json

from basic.app_str import UString
from basic.tiny_fn import alert, file_io
from matplot.basic_graphic import MatPlotUi
from matplot.function.draw_user_function import DrawUserFunction
from matplot.tools.control import Tools
from ui.math.add_math import AddMath


class MainPage:
    s_index = 0
    tools = None

    def __init__(self, page):
        self.chart = None
        self.matplot_chart = None
        UString.matplot_chart = MatPlotUi(page)
        self.display_step_input = TextField(width=40, height=40, on_submit=self.on_d_step_change,
                                            border=InputBorder.NONE,
                                            filled=True,
                                            value=UString.display_step)
        self.step_input = TextField(width=70, height=40, on_submit=self.on_step_change, suffix_text="%",
                                    border=InputBorder.NONE,
                                    filled=True,
                                    value=str(UString.step * 4))
        self.x_offset_input = TextField(width=40, height=40, on_submit=self.on_offset_change,
                                        border=InputBorder.NONE,
                                        filled=True,
                                        value=str(UString.x_offset),
                                        data="x")
        self.y_offset_input = TextField(width=40, height=40, on_submit=self.on_offset_change,
                                        border=InputBorder.NONE,
                                        filled=True,
                                        value=str(UString.y_offset),
                                        data="y")
        self.lists = UString.lists
        self.page = page

    @staticmethod
    async def on_offset_change(e):
        data = e.control.data
        if data == "x":
            UString.x_offset = float(e.control.value)
        elif data == "y":
            UString.y_offset = float(e.control.value)
        await UString.matplot_chart.update_draw()

    async def on_d_step_change(self, e):
        if float(e.control.value) <= 0:
            await alert(self.page, "错误", "间隔不能小于等于0")
        if float(e.control.value) < 0.5:
            await alert(self.page, "警告", "您将间隔调到了0.5一下,可能会导致设备卡顿,渲染时间长的问题")
            await asyncio.sleep(3)
        UString.display_step = float(e.control.value)
        await UString.matplot_chart.update_draw()

    async def on_step_change(self, e):
        if float(e.control.value) <= 0:
            await alert(self.page, "错误", "缩放不能小于等于0")
        """
        if float(e.control.value) < 0.5:
            await alert(self.page, "警告", "您将间隔调到了0.5一下,可能会导致设备卡顿,渲染时间长的问题")
            await asyncio.sleep(3)
        """
        UString.step = float(e.control.value) / 4
        await UString.matplot_chart.update_draw()

    async def matplot_ui(self):
        # 从全局变量中构建函数图像的UI，该方法在初始化/页面分辨率改变时会触发
        for content in UString.lists:
            if content["mode"] == "fx":
                DrawUserFunction(content, self.page).draw()
            if content["mode"] == "point":
                DrawUserFunction(content, self.page, "point").draw()
        self.matplot_chart = await UString.matplot_chart.update_draw()
        self.chart = Column(
            [
                Stack(
                    [
                        self.matplot_chart,
                        Row([Row(
                            [
                                Text("显示间隔"),
                                self.display_step_input,
                                Text("缩放"),
                                self.step_input,
                                Text("X偏移"),
                                self.x_offset_input,
                                Text("Y偏移"),
                                self.y_offset_input
                            ],
                            scroll=ScrollMode.ALWAYS,
                            alignment=MainAxisAlignment.CENTER,
                        )], expand=True, bottom=20, scroll=ScrollMode.ALWAYS)
                    ]
                )
            ]
        )
        return self.chart

    def nav_change(self):
        return self.chart

    async def dark_mode_change(self):
        self.matplot_chart = await UString.matplot_chart.update_draw()
        self.chart = Column(
            [
                Stack(
                    [
                        self.matplot_chart,
                        Row(
                            [
                                Text("显示间隔"),
                                self.display_step_input,
                                Text("缩放"),
                                self.step_input
                            ],
                            bottom=20,
                        )
                    ]
                )
            ]
        )
        return self.chart


async def main_page(_page, navbar):
    equals = Container()  # latex公式
    if any([UString.main_page_control is None, UString.math_list is None, MainPage.tools is None]):
        # 初次进入调用
        UString.main_page_control = MainPage(_page)
        UString.math_list = AddMath(_page, equals)
        MainPage.tools = Tools(_page)
    _control = UString.main_page_control  # 更新control
    if any([UString.nav_change, UString.change_dark]):
        # 导航更换与暗黑模式切换调用
        if UString.change_dark:
            matplot_chart = await _control.dark_mode_change()
        if UString.nav_change:
            matplot_chart = _control.nav_change()
        equals.content = UString.math_list.create_ui()
        UString.change_dark = False
        MainPage.tools.update_ui()
        tools_container = MainPage.tools.create_ui()
    else:
        # 初次进入调用
        UString.main_page_control = MainPage(_page)
        UString.math_list = AddMath(_page, equals)
        _control = UString.main_page_control
        equals.content = UString.math_list.create_ui()
        UString.matplot_chart.draw()
        matplot_chart = await _control.matplot_ui()  # 函数图像UI
        MainPage.tools.create_ui()
        tools_container = MainPage.tools.update_ui()
        if _page.width < 550:
            MainPage.tools.element.height = ((_page.height - 150) / 7) * 2.5 - 80
        else:
            MainPage.tools.element.height = _page.height - 140

    async def add(e):
        mode = e.control.data
        await UString.math_list.show_bs(None, mode)

    def tab_change(e):
        MainPage.s_index = e.control.selected_index

    async def save_canvas(e):
        file_name = TextField(border=InputBorder.UNDERLINE, filled=True)
        type = RadioGroup(Column(
            [
                Radio(value="svg", label="SVG(矢量图)"),
                Radio(value="png", label="PNG"),
                Radio(value="jpeg", label="JPEG"),
            ]
        ), value="png")

        async def ok(e):
            data = type.value
            _page.dialog.open = False
            await _page.update_async()
            name = file_name.value
            pic = UString.matplot_chart.get_pic(data)
            await file_io(_page, "save", pic, "{}.{}".format(name, data), read_m="w" if data == "svg" else "wb")

        async def cancel(e):
            _page.dialog.open = False
            await _page.update_async()
            await alert(_page, "提示", "您取消了保存")

        _page.dialog = AlertDialog(
            modal=True,
            title=Text("輸入保存文件名称"),
            content=Column([
                file_name,
                Text("类型"),
                type
            ]),
            actions=[
                TextButton("确认", on_click=ok),
                TextButton("取消", on_click=cancel)
            ],
            actions_alignment=MainAxisAlignment.END,
            open=True
        )
        await _page.update_async()

    async def save_config(e):
        file_name = TextField(border=InputBorder.UNDERLINE, filled=True)

        async def ok(e):
            _page.dialog.open = False
            await _page.update_async()
            name = file_name.value
            data = json.dumps(UString.lists)
            await file_io(_page, "save", data, "{}.json".format(name), read_m="w")

        async def cancel(e):
            _page.dialog.open = False
            await _page.update_async()
            await alert(_page, "提示", "您取消了保存")

        _page.dialog = AlertDialog(
            modal=True,
            title=Text("輸入保存文件名称"),
            content=file_name,
            actions=[
                TextButton("确认", on_click=ok),
                TextButton("取消", on_click=cancel)
            ],
            actions_alignment=MainAxisAlignment.END,
            open=True
        )
        await _page.update_async()

    def load_config(e):
        pass

    input_ui = Column(
        controls=[
            Container(
                Column(
                    [
                        equals,
                        Row(
                            controls=[
                                PopupMenuButton(
                                    icon=icons.ADD,
                                    tooltip="新建",
                                    items=[
                                        PopupMenuItem(
                                            text="函数",
                                            on_click=add,
                                            data="fx"
                                        ),
                                        PopupMenuItem(
                                            text="方程",
                                            on_click=add,
                                            data="equ"
                                        ),
                                        PopupMenuItem(
                                            text="点",
                                            on_click=add,
                                            data="point"
                                        )
                                    ]
                                )
                            ],
                            alignment=MainAxisAlignment.END
                        ),
                    ],
                    expand=True
                )
            )
        ],
        expand=True,
        alignment=MainAxisAlignment.START,
    )
    # 工具UI
    tools_ui = Column(
        controls=[
            Container(
                Column(
                    [
                        tools_container,
                        Divider(height=1),
                        Row(
                            controls=[
                                # 函数工具相关
                                PopupMenuButton(
                                    content=Container(
                                        content=Text("函数"),
                                        width=70,
                                        border=border.all(1, colors.BLUE),
                                        padding=10,
                                        border_radius=10,
                                        alignment=alignment.center
                                    ),
                                    items=[
                                        PopupMenuItem(
                                            content=Text("多项式拟合曲线"),
                                            on_click=MainPage.tools.open_bs,
                                            data="fit_poly"
                                        ),
                                        PopupMenuItem(
                                            content=Text("根据Y求X"),
                                            on_click=MainPage.tools.open_bs,
                                            data="x-call"
                                        ),
                                        PopupMenuItem(
                                            content=Text("根据X求Y"),
                                            on_click=MainPage.tools.open_bs,
                                            data="y-call"
                                        ),
                                        PopupMenuItem(
                                            content=Text("求函数交点"),
                                            on_click=MainPage.tools.open_bs,
                                            data="intersection"
                                        ),
                                        PopupMenuItem(
                                            content=Text("求函数根"),
                                            on_click=MainPage.tools.open_bs,
                                            data="root"
                                        ),
                                        PopupMenuItem(
                                            content=Text("求函数极值"),
                                            on_click=MainPage.tools.open_bs,
                                            data="limit"
                                        ),
                                    ]
                                ),
                                PopupMenuButton(
                                    content=Container(
                                        content=Text("代数"),
                                        width=70,
                                        border=border.all(1, colors.BLUE),
                                        padding=10,
                                        border_radius=10,
                                        alignment=alignment.center
                                    ),
                                    items=[
                                        PopupMenuItem(
                                            content=Text("多项式展开"),
                                            on_click=MainPage.tools.open_bs,
                                            data="expand"
                                        ),
                                        PopupMenuItem(
                                            content=Text("因式分解"),
                                            on_click=MainPage.tools.open_bs,
                                            data="factor"
                                        ),
                                        PopupMenuItem(
                                            content=Text("合并同类项"),
                                            on_click=MainPage.tools.open_bs,
                                            data="collect"
                                        ),
                                        PopupMenuItem(
                                            content=Text("有理分式化简"),
                                            on_click=MainPage.tools.open_bs,
                                            data="cancel"
                                        ),
                                    ]
                                )
                            ],
                            scroll=ScrollMode.ALWAYS,
                        ),
                    ],
                    expand=True,
                    alignment=MainAxisAlignment.END
                )
            )
        ],
        expand=True,
        alignment=MainAxisAlignment.START,
    )
    operate_ui = Column(
        [
            ElevatedButton("存储配置", on_click=save_config),
            ElevatedButton("加载配置", on_click=load_config),
            ElevatedButton("存储图像", on_click=save_canvas)
        ],
    )
    content = [Row(

        [
            navbar,
            VerticalDivider(width=1),
            Row(
                [
                    Tabs(
                        selected_index=MainPage.s_index,
                        on_change=tab_change,
                        expand=1,
                        tabs=[
                            Tab(
                                text="函数",
                                content=input_ui
                            ),
                            Tab(
                                text="工具",
                                content=tools_ui
                            ),
                            Tab(
                                text="操作",
                                content=operate_ui
                            )
                        ]
                    )
                ],
                width=((_page.width - 100) / 7) * 1.8,
                alignment=MainAxisAlignment.START,

            ),
            VerticalDivider(width=1),
            Row(
                [
                    Container(
                        matplot_chart,
                        height=_page.height,
                    )
                ],
                width=((_page.width - 100) / 7) * 5.2,
                alignment=MainAxisAlignment.START
            )
        ], expand=True
    )
    ] if _page.width > 550 else [SafeArea(
        content=Column(
            [
                Column(
                    [
                        Container(
                            matplot_chart,
                            width=_page.width,
                            height=((_page.height - 150) / 7) * 4.5
                        ),
                    ]
                ),
                Divider(height=1),
                Column(
                    [
                        Tabs(
                            on_change=tab_change,
                            selected_index=MainPage.s_index,
                            expand=1,
                            tabs=[
                                Tab(
                                    text="函数",
                                    content=input_ui
                                ),
                                Tab(
                                    text="工具",
                                    content=tools_ui
                                ),
                                Tab(
                                    text="操作",
                                    content=operate_ui
                                )
                            ]
                        )
                    ]),
            ],
        )
    ), navbar]
    View(
        "/home",
        controls=content
    )
    return content
