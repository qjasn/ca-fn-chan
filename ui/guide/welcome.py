from flet import *


async def welcome_ui(e, page: Page):
    async def next(e):
        await page.go_async("/license")

    return View(
        route="/welcome",
        controls=[
            Column([
                Row(
                    [
                        Text("欢迎使用", theme_style=TextThemeStyle.TITLE_LARGE),
                        ElevatedButton("进入引导", on_click=next)
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    expand=True
                )],
                alignment=MainAxisAlignment.CENTER,
                expand=True,
                width=page.width
            )
        ]
    )
