import flet as ft
import latexify

from lib.control import AppControl
from matplot.latex import Latex


def main(page: ft.Page):
    _AppControl = AppControl(page)
    _AppControl.init()
    page.on_route_change = _AppControl.route.change_route
    page.on_view_pop = _AppControl.route.view_pop
    page.on_resize = _AppControl.on_resize
    page.on_platform_brightness_change = _AppControl.on_resize


ft.app(target=main)
