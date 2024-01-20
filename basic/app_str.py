from flet_core import Page, ThemeMode


class UString:
    lists = []
    t = 0
    f_n = ["f", "g", "h", "p", "q", "r", "s", "t"]
    a_e = []
    width = 500
    height = 600
    step = 25
    darkMode = {
        "SYSTEM": ThemeMode.SYSTEM,
        "LIGHT": ThemeMode.LIGHT,
        "DARK": ThemeMode.DARK
    }
    resize = False
    matplot_chart = None

    def __init__(self, page: Page):
        UString.width = page.width
        UString.height = page.height
