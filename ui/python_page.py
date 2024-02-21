import asyncio
import io
import sys
import time
from os import truncate
from threading import Thread

from flet import *

from basic.app_str import UString
from basic.is_dark import is_closed


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
        self.display = Column([
            Text("Python " + sys.version + " REPl")
        ],scroll=ScrollMode.ALWAYS)
        self.running = False
        self.input_e = TextField(
            border=InputBorder.NONE,
            on_submit=self.on_submit
        )
        self.input_t = Text("> ")
        self.input = Row([self.input_t, self.input_e])
        self.code = ""

    async def on_submit(self, e):
        value = str(e.control.value)
        self.input_e.value = ""
        self.display.controls.remove(self.input)
        self.display.controls.append(Text(self.input_t.value + value + "\n"))
        await self.update_async()
        if value == "":
            await self.run()
            self.code = ""
            self.input_t.value = "> "
            self.display.controls.append(self.input)
        elif value.endswith(":"):
            self.code += "\n{}".format(value)
            self.input_t.value = "... "
            self.display.controls.append(self.input)
        elif not is_closed(self.code + "\n" + value):
            self.code += "\n{}".format(value)
            self.input_t.value = "... "
            self.display.controls.append(self.input)
        else:
            self.code = value
            await self.run()
            self.code = ""
            self.input_t.value = "> "
            self.display.controls.append(self.input)
        await self.update_async()
        await self.input_e.focus_async()

    async def did_mount_async(self):
        self.running = True
        self.temp_io = [self.ioString_out.getvalue(), self.ioString_err.getvalue(), self.ioString_err.getvalue()]
        self.display.controls.append(self.input)
        await self.update_async()
        # noinspection PyAsyncCall
        asyncio.create_task(self.on_write())

    async def on_write(self):
        while self.running:
            await asyncio.sleep(0.01)
            if self.ioString_out.getvalue() != "":
                temp = self.ioString_out.getvalue()
                self.ioString_out.close()
                self.display.controls.append(Text(temp))
                await self.update_async()
                self.ioString_out = io.StringIO()
            if self.ioString_err.getvalue() != "":
                temp = self.ioString_err.getvalue()
                self.ioString_err.close()
                self.display.controls.append(Text(temp,color=colors.RED))
                await self.update_async()
                self.ioString_err = io.StringIO()
                await self.update_async()

    async def will_unmount_async(self):
        self.running = False

    async def run(self):
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = self.ioString_out
        sys.stderr = self.ioString_err
        await self.exec()
        sys.stdout, sys.stderr = old_stdout, old_stderr

    async def exec(self):
        exec(self.code, PythonRepl._locals, PythonRepl._globals)

    def build(self):
        return self.display


def python_page(_page, navbar):
    if UString.python_repl is None:
        UString.python_repl = PythonRepl()
    repl = UString.python_repl

    content = Column([
        repl,
    ])

    return [Row([
        navbar, VerticalDivider(width=1), content
    ], expand=True)] if _page.width > 550 else [SafeArea(content), navbar]
