from flet import *

from basic.app_str import UString


def python_page(_page, navbar):
    content = Column(

    )

    return [Row([
        navbar, VerticalDivider(width=1), content
    ], expand=True)] if _page.width > 550 else [SafeArea(content), navbar]
