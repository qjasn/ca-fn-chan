from flet import *


async def teach_ui(page):
    async def next(e):
        await page.go_async("/")
    return View(
        route="/teach",
        controls=[
            ElevatedButton("next",on_click=next)
        ]
    )