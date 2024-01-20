from flet import *

from basic.app_str import UString


def settings_page(_page, navbar):
    def dark_mode_change(e):
        # 单选更新后触发
        _mode = _page.client_storage.get("fx.darkMode")
        _page.client_storage.set("fx.darkMode", e.control.value)
        _page.theme_mode = UString.darkMode[e.control.value]
        _page.update()

    dark_mode_ui = RadioGroup(Column([
        Radio(value="SYSTEM", label="跟随系统"),
        Radio(value="LIGHT", label="明亮"),
        Radio(value="DARK", label="暗黑")

    ], alignment=MainAxisAlignment.START),
        value=_page.client_storage.get("fx.darkMode"),
        on_change=dark_mode_change
    )
    content = Column(
        [Column([
            ListTile(title=Text("设置")),
            ListTile(leading=Icon(icons.DARK_MODE), title=Text("暗黑模式")),
            Divider(height=1),
            dark_mode_ui
        ],
            alignment=MainAxisAlignment.START)],
        alignment=MainAxisAlignment.START,
        expand=True
    )

    return [Row([
        navbar, VerticalDivider(width=1), content
    ], expand=True)] if _page.width > 550 else [SafeArea(content), navbar]
