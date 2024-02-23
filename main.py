import flet as ft

from basic.app_str import UString
from basic.control import AppControl


async def main(page: ft.Page):
    # 实例化总控类
    _AppControl = AppControl(page)
    await _AppControl.init()
    UString(page)
    # 分别设置flet的响应项目
    page.on_route_change = _AppControl.route.change_route
    page.on_view_pop = _AppControl.route.view_pop

    async def on_resize(e):
        await _AppControl.on_resize(None)
        UString(page)

    page.on_resize = on_resize

    async def dark_change(e):
        UString.change_dark = True
        _AppControl.route.update_ui()
        await page.update_async()

    page.on_platform_brightness_change = dark_change


ft.app(target=main)
