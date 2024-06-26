import flet as ft

class State:
    toggle = True

s = State()

def main(page: ft.Page):
    data_1 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, 3),
                ft.LineChartDataPoint(2.6, 2),
                ft.LineChartDataPoint(4.9, 5),
                ft.LineChartDataPoint(6.8, 3.1),
                ft.LineChartDataPoint(8, 4),
                ft.LineChartDataPoint(9.5, 3),
                ft.LineChartDataPoint(11, 4),
            ],
            stroke_width=5,
            color=ft.colors.CYAN,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    data_2 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, 3.44),
                ft.LineChartDataPoint(2.6, 3.44),
                ft.LineChartDataPoint(4.9, 3.44),
                ft.LineChartDataPoint(6.8, 3.44),
                ft.LineChartDataPoint(8, 3.44),
                ft.LineChartDataPoint(9.5, 3.44),
                ft.LineChartDataPoint(11, 3.44),
            ],
            stroke_width=5,
            color=ft.colors.CYAN,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    chart = ft.LineChart(
        horizontal_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=1, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=1
        ),
        left_axis=ft.ChartAxis(
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels_interval=10,
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=6,
        min_x=0,
        max_x=11,
        # animate=5000,
        expand=True,
    )

    def toggle_data(e):
        if s.toggle:
            chart.data_series = data_2
            chart.interactive = False
        else:
            chart.data_series = data_1
            chart.interactive = True
        s.toggle = not s.toggle
        chart.update()

    page.add(ft.ElevatedButton("avg", on_click=toggle_data), chart)

ft.app(main)