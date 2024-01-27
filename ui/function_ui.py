from flet_core import *

from basic.app_str import UString
from matplot.latex import Latex


# 该类主要负责构建函数表达式的控件
class FunctionUI:
    delete = []

    def __init__(self, name, args, text, page, subscript=False):
        self.lists = UString.lists
        self.ui = None
        self.equation = {
            "name": name,
            "args": args,
            "text": text
        }  # 设置此类预备转化为latex的对象，其中说明见 basic/app_str.py
        self.page = page
        self.latex = Latex(name=name, args=args, text=text, page=page)  # 将参数转化为latex
        self.latex.init(subscript)  # 初始化Latex类
        self.latex_image = self.latex.output_svg()[0]  # 获取渲染后的svg图像
        self.h = self.latex.output_svg()[1]

    def on_change(self, e):
        UString.draw_class[self.equation["name"]].visible(e.control.value)
        UString.matplot_chart.update_draw()  # 更新UI
        self.page.update()

    def on_click(self, _list=None, element=None):
        # 该函数在点击 删除 时调用
        UString.lists.remove(_list)  # 从lists删除对应的结构化函数
        UString.draw_class[_list["name"]].delete()  # 清除函数图像
        UString.a_e.remove(_list["name"])  # 删除存在的函数名称
        UString.draw_class.pop(_list["name"])
        element.content.controls.remove(self.ui)  # 从页面删除此元素
        UString.matplot_chart.update_draw()  # 更新UI
        self.page.update()

    def create_ui(self, _list, element):
        # 构建UI
        self.ui = Row(
            [
                Stack([
                    Row([
                        Checkbox(
                            value=True,
                            on_change=self.on_change

                        ),
                        Container(
                            content=self.latex_image,
                            height=self.h
                        )
                    ], scroll=ScrollMode.ALWAYS,
                        width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (
                                self.page.width - 55),

                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="删除",
                                on_click=lambda e: self.on_click(_list, element)
                            )
                        ]

                        ), right=0 if self.page.width > 550 else 20,

                    )
                ], width=(((self.page.width - 100) / 7) * 1.8) if self.page.width > 550 else self.page.width,
                )
            ]
        )
        return self.ui
