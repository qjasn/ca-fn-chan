import flet as ft

from basic.app_str import UString
from basic.navigation import Navigation

# 总控Class
class AppControl:
    lists = []

    def __init__(self, page: ft.Page):
        self.page = page
        # 实例化导航Class
        self.route = Navigation(page)

    def init(self):
        # 初始化整个页面
        _page = self.page
        UString.width = self.page.width
        UString.height = self.page.height
        _page.title = "graphical calc" # 设置应用标题
        # 查看是否自定义设置了UI显示类型
        if _page.client_storage.get("fx.darkMode") is None:
            _page.client_storage.set("fx.darkMode", "SYSTEM")
        _page.theme_mode = UString.darkMode[_page.client_storage.get("fx.darkMode")]
        # 初始化路由
        self.route.init_route()
        _page.update()

    def on_resize(self, resize):
        # 页面分辨率更新时触发
        UString.resize = True # 设置 分辨率更新模式 为True
        UString.width = self.page.width
        UString.height = self.page.height
        _page = self.page
        self.route.update_ui() # 更新页面UI
        UString.resize = False
        _page.update()
