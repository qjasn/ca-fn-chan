from flet import *

from matplot.latex.latex import latex_ui


async def teach_ui(page: Page):
    async def next(e):
        await page.client_storage.set_async("fx.start", True)
        await page.go_async("/")

    return View(
        route="/teach",
        controls=[
            Column(
                [
                    Row(
                        [
                            Column(
                                [
                                    Row(
                                        [
                                            Text("输入公式教程", theme_style=TextThemeStyle.TITLE_LARGE)
                                        ]
                                    ),
                                    Row(
                                        [
                                            Text("此应用使用Python表达式作为输入模式")
                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    ),
                                    Row(
                                        [
                                            Text("平方立方输入:"),
                                            Text("x**2"),
                                            Icon(icons.ARROW_RIGHT_ALT),
                                            Container(
                                                content=latex_ui(page, "x^2")[0],
                                                height=latex_ui(page, "x^2")[1],
                                            )
                                        ]
                                    ),
                                    Row(
                                        [
                                            Text("符号输入:"),
                                            Text("sqrt(x)"),
                                            Icon(icons.ARROW_RIGHT_ALT),
                                            Container(
                                                content=latex_ui(page, r"\sqrt{x}")[0],
                                                height=latex_ui(page, r"\sqrt{x}")[1],
                                            )
                                        ]
                                    ),
                                    ElevatedButton("我已知晓,进入应用", on_click=next)
                                ]
                            )
                        ],
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                expand=True
            )
        ]
    )
