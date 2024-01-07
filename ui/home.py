import io

from flet import *
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("svg")


def home_page(page, navbar):
    fig, ax = plt.subplots()

    fruits = ["apple", "blueberry", "cherry", "orange"]
    counts = [40, 100, 30, 55]
    bar_labels = ["red", "blue", "_red", "orange"]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel("fruit supply")
    ax.set_title("Fruit supply by kind and color")
    ax.legend(title="Fruit color")
    s = io.StringIO()
    fig.savefig(s, format="svg", transparent=True)
    svg = s.getvalue()
    matplotlib_chart = Image(src=svg, visible=True)

    def show_chart(e):
        matplotlib_chart.visible = True
        page.update()

    content = [Row(
            [
                navbar,
                VerticalDivider(width=1),
                Column(
                    [
                        Text("Hello world"),
                        ElevatedButton("Show Chart", on_click=show_chart),
                    ]),
                Container(
                    matplotlib_chart,
                    bgcolor=colors.YELLOW,

                )
            ],expand=True
        )
    ] if page.width > 550 else [SafeArea(
        content=Column(
            [
                Container(
                    matplotlib_chart,
                    bgcolor=colors.YELLOW,

                ),
                Row(
                    [
                        Text("Hello world"),
                        ElevatedButton("Show Chart", on_click=show_chart),
                    ]),
            ],
        )
    ), navbar]
    view = View(
        "/home",
        controls=content
    )
    return content
