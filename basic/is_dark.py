import flet as ft

# 该函数用来确认页面是否处于暗黑模式状态
def is_dark(page: ft.Page):
    print(page.platform_brightness)
    if page.theme_mode == ft.ThemeMode.SYSTEM:
        if page.platform_brightness == ft.ThemeMode.DARK:
            return True
        else:
            return False
    elif page.theme_mode == ft.ThemeMode.DARK:
        return True
    else:
        return False
