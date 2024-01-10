from flet import *


def settings_page(_page, navbar):
    def dark_mode_change(e):
        _mode = _page.client_storage.get("fx.darkMode")
        _page.client_storage.set("fx.darkMode", e.control.value)
        _page.theme_mode = e.control.value
        _page.update()

    dark_mode_ui = RadioGroup(Column([
        Radio(value="SYSTEM", label="System"),
        Radio(value="LIGHT", label="Light"),
        Radio(value="DARK", label="Dark")

    ], alignment=MainAxisAlignment.START),
        value=_page.client_storage.get("fx.darkMode"),
        on_change=dark_mode_change
    )
    content = Column(
        [Column([
            ListTile(title=Text("Settings")),
            ListTile(leading=Icon(icons.DARK_MODE), title=Text("DarkMode")),
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
