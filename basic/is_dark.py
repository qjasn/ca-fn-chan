import flet as ft


# 该函数用来确认页面是否处于暗黑模式状态
def is_dark(page: ft.Page):
    if page.theme_mode == ft.ThemeMode.SYSTEM:
        if page.platform_brightness == ft.ThemeMode.DARK:
            return True
        else:
            return False
    elif page.theme_mode == ft.ThemeMode.DARK:
        return True
    else:
        return False


def is_closed(text: str) -> bool:
    stack = []
    brackets = {')': '(', ']': '[', '}': '{'}
    for char in text:
        if char in brackets.values():
            stack.append(char)
        elif char in brackets.keys():
            if brackets[char] != stack.pop():
                return False
    return True
