import asyncio
import io
import sys
from threading import Thread

from flet import *

from basic.app_str import UString


class PythonRepl(UserControl):
    _globals = dict()
    _locals = dict()

    def __init__(self):
        super().__init__()
        self.code = None
        self.task = None
        self.ioString_out = io.StringIO()
        self.ioString_err = io.StringIO()
        self.ioString_in = io.StringIO()
        self.temp_io = [self.ioString_out.getvalue(), self.ioString_err.getvalue(), self.ioString_err.getvalue()]
        self.display = Column(scroll=ScrollMode.ALWAYS)
        self.running = False

    async def did_mount_async(self):
        self.running = True
        for i in self.ioString_out.getvalue().split("\n"):
            self.display.controls.append(Text(i))
        self.temp_io = [self.ioString_out.getvalue(), self.ioString_err.getvalue(), self.ioString_err.getvalue()]
        await self.update_async()
        # noinspection PyAsyncCall
        asyncio.create_task(self.on_write())

    async def on_write(self):
        print("on write")
        while self.running:
            if self.ioString_out.getvalue() != self.temp_io[0]:
                self.temp_io[0] = self.ioString_out.getvalue()
                self.display.controls.append(Text(self.temp_io[0].split("\n")[-2]))
                await self.update_async()
            if self.ioString_err.getvalue() != self.temp_io[1]:
                self.temp_io[1] = self.ioString_err.getvalue()
                self.display.controls.append(Text(self.temp_io[1].split("\n")[-2], color=colors.RED))
                await self.update_async()

    async def will_unmount_async(self):
        self.running = False
        self.display.controls = []
        await self.update_async()

    def run(self, code):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = self.ioString_out
        sys.stderr = self.ioString_err
        self.code = code
        thread = Thread(target=self.exec)
        thread.start()
        thread.join()
        sys.stdout, sys.stderr = old_stdout, old_stderr

    def exec(self):
        exec(self.code, PythonRepl._locals, PythonRepl._globals)

    def build(self):
        return self.display


def python_page(_page, navbar):
    if UString.python_repl is None:
        UString.python_repl = PythonRepl()
        UString.python_repl.ioString_out.write("Python " + sys.version + " REPl")
    repl = UString.python_repl

    input_e = TextField(
        # icon=icons.KEYBOARD_ARROW_RIGHT,
        multiline=True,
        max_lines=5,
        border=InputBorder.NONE
    )

    content = Column([
        repl
    ])

    return [Row([
        navbar, VerticalDivider(width=1), content
    ], expand=True)] if _page.width > 550 else [SafeArea(content), navbar]
