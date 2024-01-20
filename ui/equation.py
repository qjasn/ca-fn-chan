from flet_core import *

from basic.app_str import UString
from matplot.basic_graphic import MatPlotUi
from matplot.draw_user_function import DrawUserFunction
from matplot.latex import Latex

# 该类主要负责控制渲染Latex
class EquationUI:
    delete = []

    def __init__(self, name, args, text, page, subscript=False):
        self.lists = UString.lists
        self.ui = None
        self.equation = {
            "name": name,
            "args": args,
            "text": text
        } # 设置此类预备转化为latex的对象，其中说明见 basic/app_str.py
        self.page = page
        self.latex = Latex(name=name, args=args, text=text, page=page) # 将参数转化为latex
        self.latex.init(subscript) # 初始化Latex类
        self.latex_image = self.latex.output_svg() # 获取渲染后的svg图像

    def on_change(self, e):
        print(self)

    def on_click(self, _list=None, element=None):
        # 该函数在点击delete时调用
        UString.lists.remove(_list) # 从lists删除对应的结构化函数
        print(UString.a_e)
        UString.a_e.remove(_list["name"]) # 删除存在的函数名称
        element.content.controls.remove(self.ui) # 从页面删除此元素
        UString.matplot_chart.draw(True) # 清除函数图像
        # 在移除之后重新绘制函数图像
        for content in UString.lists:
            DrawUserFunction(content, self.page).draw(UString.matplot_chart.return_ax())
        UString.matplot_chart.update_draw() #更新UI
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
                            height=20
                        )
                    ], scroll=ScrollMode.ALWAYS,
                        width=(((self.page.width - 100) / 7) * 1.8 - 35) if self.page.width > 550 else (
                                self.page.width - 55),

                    ),
                    Container(
                        content=PopupMenuButton(items=[
                            PopupMenuItem(
                                text="Delete",
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
