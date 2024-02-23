import uuid

from flet import *

from matplot.tools.algebra import *
from matplot.tools.calc_function import *
from matplot.tools.fitploy import FitPolyUi
from matplot.tools.limit_fn import Limit

"""
通用说明：
对于构建工具的Class说明：
1. 要有构建输入框UI的函数（即下面的fit_poly_ui）
2. 要有onclick(async)函数，需要返回一个flet ui实例,其中存储结果相关内容至self
3. 要有update_ui函数，返回一个flet ui实例，内容与onclick返回的内容相同，但使用的是self已经算好的内容
"""


class Tools:
    tool_lists = []
    running_class = []

    def __init__(self, _page: Page):
        self.ok = True
        self.page = _page
        self.ok_button = TextButton("确认")
        self.bs_content = Row(
            scroll=ScrollMode.ALWAYS,
            controls=[
                Container(
                    padding=10,
                )
            ],
        )
        self.element = Column(
            alignment=MainAxisAlignment.START,
            height=self.page.height - 140,
            controls=[]
        )

        self.bs = BottomSheet(
            Container(
                Column([
                    Divider(height=1),
                    self.bs_content,
                    Row(
                        [
                            TextButton("取消", on_click=self.cancel_button),
                            self.ok_button
                        ]
                    )
                ],
                    tight=True),
                padding=10,
            ),
            on_dismiss=self.dismiss,
        )
        _page.overlay.append(self.bs)

    async def close_bs(self, e, cancel=False):
        self.bs.open = False
        await self.bs.update_async()

    async def dismiss(self, e):
        if not self.ok:
            Tools.running_class.remove(Tools.running_class[-1])

    def ok_button_click(self):
        self.ok = True

    async def cancel_button(self, e):
        self.ok = False
        await self.close_bs(None, False)

    async def onclick(self, e):
        Tools.tool_lists.append(await Tools.running_class[-1].onclick(self.element, Tools.tool_lists,
                                                                      Tools.running_class))
        self.create_ui()
        await self.page.update_async()
        self.ok_button_click()
        await self.close_bs(None)

    async def open_bs(self, e):
        mode = e.control.data
        if mode == "fit_poly":
            Tools.running_class.append(FitPolyUi(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=await Tools.running_class[-1].fit_poly_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "expand":
            Tools.running_class.append(Expand(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].expand_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "factor":
            Tools.running_class.append(Factor(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].expand_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "collect":
            Tools.running_class.append(Collect(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].expand_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "cancel":
            Tools.running_class.append(Cancel(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].expand_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick,
        elif mode == "x-call":
            Tools.running_class.append(XCall(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].xcall_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "y-call":
            Tools.running_class.append(YCall(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].ycall_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "intersection":
            Tools.running_class.append(Intersection(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].intersection_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "root":
            Tools.running_class.append(Root(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].root_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        elif mode == "limit":
            Tools.running_class.append(Limit(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=await Tools.running_class[-1].limit_ui()
            )
            self.ok = False
            self.ok_button.on_click = self.onclick
        self.bs.open = True
        await self.bs.update_async()

    def create_ui(self):
        self.element.controls = []
        for i in Tools.tool_lists:
            self.element.controls.append(i)
        return self.element

    def update_ui(self):
        Tools.tool_lists = []
        for i in Tools.running_class:
            Tools.tool_lists.append(i.update_ui(self.element, Tools.tool_lists, Tools.running_class))
        self.element.controls = []
        for i in Tools.tool_lists:
            self.element.controls.append(i)
        return self.element
