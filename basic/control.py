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

    async def init(self):
        # 初始化整个页面
        _page = self.page
        UString.width = self.page.width
        UString.height = self.page.height
        _page.title = "graphical calc"  # 设置应用标题
        # 查看是否自定义设置了UI显示类型
        if await _page.client_storage.get_async("fx.darkMode") is None:
            await _page.client_storage.set_async("fx.darkMode", "SYSTEM")
        if await _page.client_storage.get_async("fx.liner") is None:
            await _page.client_storage.set_async("fx.liner", "liner-sci-liner")
        if await _page.client_storage.get_async("fx.polynomial") is None:
            await _page.client_storage.set_async("fx.polynomial", "polynomial-num-polyfit")
        if await _page.client_storage.get_async("fx.fourier") is None:
            await _page.client_storage.set_async("fx.fourier", "enable-fourier")
        if await _page.client_storage.get_async("fx.limit") is None:
            await _page.client_storage.set_async("fx.limit", "sym-derivative")
        _page.theme_mode = UString.darkMode[await _page.client_storage.get_async("fx.darkMode")]
        # 初始化路由
        await self.route.init_route()
        await _page.update_async()

    async def on_resize(self, resize):
        # 页面分辨率更新时触发
        UString.resize = True  # 设置 分辨率更新模式 为True
        UString.width = self.page.width
        UString.height = self.page.height
        _page = self.page
        await self.route.update_ui()  # 更新页面UI
        UString.resize = False
        await _page.update_async()
