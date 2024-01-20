import flet as ft

from basic.app_str import UString
from basic.control import AppControl


def main(page: ft.Page):
    # 实例化总控类
    _AppControl = AppControl(page)
    _AppControl.init()
    UString(page)
    # 分别设置flet的响应项目
    page.on_route_change = _AppControl.route.change_route
    page.on_view_pop = _AppControl.route.view_pop
    page.on_resize = lambda e: (
        _AppControl.on_resize(None),
        UString(page)
    )
    page.on_platform_brightness_change = _AppControl.on_resize


ft.app(target=main)
