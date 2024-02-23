import flet as ft
from flet_core import AlertDialog, Text


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


async def alert(_page, title: str, tip: str):
    _page.dialog = AlertDialog(
        modal=False,
        title=Text(title),
        content=Text(tip),
        open=True,

    )
    await _page.update_async()


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


async def file_io(page: ft.Page, method: str, content: str | bytes, name="save", read_m="w", fn=None):
    async def on_result(e):
        path = e.path
        method = e.control.data
        if method == "save":
            if path is not None:
                f = open(r"{}".format(path), read_m)
                f.write(content)
                f.close()
            else:
                await alert(page, "提示", "您取消了保存")
        elif method == "load":
            if path is not None:
                f = open(r"{}/{}".format(path, name), read_m)
                result = f.read()
                if fn is not None:
                    opr = fn
                    opr(result)
            else:
                await alert(page, "提示", "您取消了加載")
        page.overlay.remove(file)
        await page.update_async()

    file = ft.FilePicker(on_result=on_result, data=method)
    page.overlay.append(file)
    await page.update_async()
    if method == "save":
        await file.save_file_async(file_name=name)
    elif method == "choose":
        await file.get_directory_path_async()
    elif method == "load":
        await file.pick_files_async()
