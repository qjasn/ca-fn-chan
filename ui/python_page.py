import asyncio
import io
import time

from flet import *

from basic.app_str import UString


class PythonRepl:
    loop = asyncio.new_event_loop()

    def __init__(self, page):
        self.ioString = io.StringIO()
        self.temp_io = self.ioString.getvalue()
        self.display = Column(scroll=ScrollMode.ALWAYS)
        self.running = False
        self.page = page
        asyncio.set_event_loop(PythonRepl.loop)

    def start(self, e):
        asyncio.run(self.start_async(None))

    async def start_async(self, e):
        self.running = True
        # noinspection PyAsyncCall
        await asyncio.create_task(self.on_write())

    async def on_write(self):
        print("start")
        while self.running:
            if self.ioString.getvalue() != self.temp_io:
                self.temp_io = self.ioString.getvalue()
                self.display.controls = []
                for i in self.temp_io.split("\n"):
                    self.display.controls.append(Text(i))
                self.display.update()

    def clear(self):
        self.running = False
        self.display.controls = []
        self.display.update()


def python_page(_page, navbar):
    if UString.python_repl is None:
        UString.python_repl = PythonRepl(_page)

    repl = UString.python_repl
    input_e = TextField()

    def write(e):
        value = input_e.value
        i = repl.ioString
        i.write(value + "\n")

    def test_write(e):
        for l in range(0, 100):
            i = repl.ioString
            i.write(str(l) + "\n")
            content.scroll_to(offset=-1, duration=100, curve=AnimationCurve.EASE_IN_OUT)
            time.sleep(0.1)

    content = Column(
        [
            ElevatedButton("start", on_click=repl.start),
            input_e,
            Row(
                [
                    ElevatedButton("write", on_click=write),
                    ElevatedButton("test write", on_click=test_write)
                ]
            ),
            Container(
                repl.display
            )
        ],
        expand=True,
        scroll=ScrollMode.ALWAYS
    )

    return [Row([
        navbar, VerticalDivider(width=1), content
    ], expand=True)] if _page.width > 550 else [SafeArea(content), navbar]
