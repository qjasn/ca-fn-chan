from flet import TemplateRoute
import flet as ft

from basic.app_str import UString
from ui.main_page import main_page
from ui.python_page import python_page
from ui.settings import settings_page


# 该Class负责应用整体的导航（路由），即多页面的切换
class Navigation:
    def __init__(self, page:ft.Page):
        self.index = 0  # 导航栏的选定值
        self.navbar = None  # 导航栏的定义，在self.nav_init_ui中得到具体的值
        self.content = "root"  # 当前页面的名称
        self.page = page  # 获取页面page控制的引用
        self.root_view = ft.View(
            '/',
            controls=[ft.Text("Loading Page")]
        )  # 根视图的ui与其引用

    async def init_route(self):
        # 初始化路由
        _page = self.page
        _t_route = TemplateRoute(_page.route)
        # 进入主页面
        await self.change_route(None)

    async def change_route(self, route):
        # 路由被改变时触发的函数
        _page = self.page
        # flet提供的路由模版
        _t_route = TemplateRoute(_page.route)
        _root_view = self.root_view
        if _t_route.match("/"):
            # 页面根目录的渲染
            _page.views.clear()
            _page.views.append(_root_view)
            await _page.update_async()
            self.root_view = _root_view
            home = await main_page(_page, self.nav_ui_init())  # 调用main_page构建ui
            self.root_view.controls = home
            self.content = "home"  # 设置目前页面名称
            await self.root_view.update_async()
            self.root_view = _root_view
            await _page.update_async()
        elif _t_route.match("/home"):
            # 页面home目录的渲染，实际与根目录一致
            home = await main_page(_page, self.nav_ui_init())
            _root_view.controls = home
            self.content = "home"
            await _root_view.update_async()
            self.root_view = _root_view
        elif _t_route.match("/settings"):
            # 页面设置目录的渲染
            settings = await settings_page(_page, self.nav_ui_init())
            _root_view.controls = settings
            self.content = "settings"
            await _root_view.update_async()
            self.root_view = _root_view
        elif _t_route.match("/python"):
            # 页面设置目录的渲染
            settings = await python_page(_page, self.nav_ui_init())
            _root_view.controls = settings
            self.content = "python"
            await _root_view.update_async()
            self.root_view = _root_view
        else:
            # 该情况只会在网页端出现，用来反馈不存在该页面
            print("404 not found")
        await _page.update_async()

    async def view_pop(self, view):
        # 返回上一个页面的函数
        self.page.views.pop()
        top_view = self.page.views[-1]
        await self.page.go_async(top_view.route)

    async def update_ui(self):
        # 更新页面UI，该函数只会在应用分辨率改变时触发，为了使UI适应新的分辨率
        _page = self.page
        _content = self.content
        _root_view = self.root_view
        if _content == "root":
            await _root_view.update_async()
        elif _content == "home":
            _root_view.controls = main_page(_page, self.nav_ui_init())
            await _root_view.update_async()
        elif _content == "python":
            _root_view.controls = python_page(_page, self.nav_ui_init())
            await _root_view.update_async()
        elif _content == "settings":
            _root_view.controls = settings_page(_page, self.nav_ui_init())
            await _root_view.update_async()
        await _page.update_async()

    async def nav_change(self, e):
        # 在导航栏的选项改变时触发
        UString.nav_change = True
        self.index = self.navbar.selected_index
        if self.navbar.selected_index == 0:
            await self.page.go_async("/home")
        elif self.navbar.selected_index == 1:
            await self.page.go_async("/python")
        else:
            await self.page.go_async("/settings")
        UString.nav_change = False

    def nav_ui_init(self):
        # 构建导航栏的UI
        if self.page.width < 550:
            # 小于550的时候使用底部导航栏
            self.navbar = ft.NavigationBar(
                selected_index=self.index,
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.FUNCTIONS, label="f(x)"),
                    ft.NavigationDestination(icon=ft.icons.CODE, label="Python"),
                    ft.NavigationDestination(icon=ft.icons.SETTINGS, label="设置")
                ],
                on_change=self.nav_change
            )
            return self.navbar
        else:
            # 大于550的时候使用侧边导航栏
            self.navbar = ft.NavigationRail(
                selected_index=self.index,
                on_change=self.nav_change,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100,
                group_alignment=-0.9,
                height=self.page.height,
                destinations=[
                    ft.NavigationRailDestination(icon=ft.icons.FUNCTIONS, label="f(x)"),
                    ft.NavigationRailDestination(icon=ft.icons.CODE, label="Python"),
                    ft.NavigationRailDestination(icon=ft.icons.SETTINGS, label="设置")
                ]
            )
            return self.navbar
