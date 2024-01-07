import flet as ft
from lib.control import AppControl



def main(page: ft.Page):
    _AppControl = AppControl(page)
    _AppControl.init()
    page.on_route_change = _AppControl.route.change_route
    page.on_view_pop = _AppControl.route.view_pop
    page.on_resize = _AppControl.on_resize


ft.app(target=main)
