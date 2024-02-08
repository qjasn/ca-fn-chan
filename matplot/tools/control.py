from flet import *

from matplot.tools.fitploy import FitPolyUi


class Tools:
    tool_lists = []
    running_class = None

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
            alignment=MainAxisAlignment.START
        )

        self.bs = BottomSheet(
            Container(
                Column([
                    Divider(height=1),
                    self.bs_content,
                    Row(
                        [
                            TextButton("取消", on_click=self.close_bs),
                            self.ok_button
                        ]
                    )
                ],
                    tight=True),
                padding=10,
            ),
        )
        _page.overlay.append(self.bs)

    def close_bs(self, e):
        self.bs.open = False
        self.bs.update()

    def open_bs(self, mode):
        if mode == "fit_poly":
            Tools.running_class = FitPolyUi(self.bs, self.page)
            self.bs_content.controls[0].content = Row(
                controls=Tools.running_class.fit_poly_ui()
            )
            self.ok_button.on_click = lambda x: (
                self.close_bs(None),
                Tools.tool_lists.append(Tools.running_class.onclick()),
                self.create_ui(),
            )
            print(Tools.tool_lists)
        self.bs.open = True
        self.bs.update()

    def create_ui(self):
        self.element.controls = []
        for i in Tools.tool_lists:
            self.element.controls.append(i)
        self.page.update()
        return self.element
