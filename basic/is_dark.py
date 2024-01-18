import flet as ft


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
