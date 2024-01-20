from flet import TemplateRoute
import flet as ft
from ui.main_page import main_page, MainPage
from ui.settings import settings_page


class Navigation:
    def __init__(self, page):
        self.index = 0
        self.navbar = None
        self.content = "root"
        print("Load navigation class")
        self.page = page
        self.root_view = ft.View(
            '/',
            controls=[ft.Text("Loading Page")]
        )

    def init_route(self):
        _page = self.page
        _t_route = TemplateRoute(_page.route)
        self.change_route(None)

    def change_route(self, route):
        print(route)
        _page = self.page
        _t_route = TemplateRoute(_page.route)
        _root_view = self.root_view
        if _t_route.match("/"):
            _page.views.clear()
            _page.views.append(_root_view)
            _page.update()
            self.root_view = _root_view
            home = main_page(_page, self.nav_ui_init())
            self.root_view.controls = home
            self.content = "home"
            print(self.root_view.controls)
            self.root_view.update()
            self.root_view = _root_view
            _page.update()
        elif _t_route.match("/home"):
            home = main_page(_page, self.nav_ui_init())
            _root_view.controls = home
            self.content = "home"
            print(_root_view.controls)
            _root_view.update()
            self.root_view = _root_view
        elif _t_route.match("/settings"):
            settings = settings_page(_page, self.nav_ui_init())
            _root_view.controls = settings
            self.content = "settings"
            _root_view.update()
            self.root_view = _root_view

        else:
            print("404 not found")
        _page.update()

    def view_pop(self, view):
        print(view)
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)

    def update_ui(self):
        _page = self.page
        _content = self.content
        _root_view = self.root_view
        if _content == "root":
            _root_view.update()
        elif _content == "home":
            _root_view.controls = main_page(_page, self.nav_ui_init())
            _root_view.update()
        elif _content == "settings":
            _root_view.controls = settings_page(_page, self.nav_ui_init())
            _root_view.update()
        _page.update()

    def nav_change(self, e):
        print(e)
        self.index = self.navbar.selected_index
        if self.navbar.selected_index == 0:
            self.page.go("/home")
        else:
            self.page.go("/settings")

    def nav_ui_init(self):
        if self.page.width < 550:
            self.navbar = ft.NavigationBar(
                selected_index=self.index,
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.FUNCTIONS, label="f(x)"),
                    ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Settings")
                ],
                on_change=self.nav_change
            )
            return self.navbar
        else:
            self.navbar = ft.NavigationRail(
                selected_index=self.index,
                on_change=self.nav_change,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100,
                group_alignment=-0.9,
                height=self.page.height,
                destinations=[
                    ft.NavigationRailDestination(icon=ft.icons.FUNCTIONS, label="f(x)"),
                    ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="Settings")
                ]
            )
            return self.navbar
