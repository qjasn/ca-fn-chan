from flet import *


async def welcome_ui(e, page: Page):
    async def next(e):
        await page.go_async("/license")

    return View(
        route="/welcome",
        controls=[
            ElevatedButton("Next", on_click=next)
        ]
    )
