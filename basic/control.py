import flet as ft

from basic.app_str import UString
from basic.navigation import Navigation


class AppControl:
    lists = []

    def __init__(self, page: ft.Page):
        self.page = page
        self.route = Navigation(page)

    def init(self):
        _page = self.page
        UString.width = self.page.width
        UString.height = self.page.height
        _page.title = "graphical calc"
        if _page.client_storage.get("fx.darkMode") is None:
            _page.client_storage.set("fx.darkMode", "SYSTEM")
        _page.theme_mode = UString.darkMode[_page.client_storage.get("fx.darkMode")]
        self.route.init_route()
        _page.update()

    def on_resize(self, resize):
        UString.width = self.page.width
        UString.height = self.page.height
        _page = self.page
        self.route.update_ui()
        _page.update()
