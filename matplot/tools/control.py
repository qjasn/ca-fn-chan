from flet import *

from matplot.tools.fitploy import FitPolyUi


class Tools:
    tool_lists = []
    running_class = []

    def __init__(self, _page: Page):
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
            controls=[]
        )

        self.bs = BottomSheet(
            Container(
                Column([
                    Divider(height=1),
                    self.bs_content,
                    Row(
                        [
                            TextButton("取消", on_click=lambda e: self.close_bs(None, True)),
                            self.ok_button
                        ]
                    )
                ],
                    tight=True),
                padding=10,
            ),
            dismissible=True
        )
        _page.overlay.append(self.bs)

    def close_bs(self, e, cancel=False):
        if cancel:
            Tools.running_class.remove(Tools.running_class[-1])
        self.bs.open = False
        self.bs.update()

    def open_bs(self, mode):
        if mode == "fit_poly":
            Tools.running_class.append(FitPolyUi(self.bs, self.page))
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class[-1].fit_poly_ui()
            )
            self.ok_button.on_click = lambda x: (
                self.close_bs(None),
                Tools.tool_lists.append(Tools.running_class[-1].onclick(self.element, Tools.tool_lists,
                                                                        Tools.running_class)),
                self.create_ui(),
                self.element.update()
            )
        self.bs.open = True
        self.bs.update()

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
