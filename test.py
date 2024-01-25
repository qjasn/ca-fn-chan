from flet import *


def main(page: Page):
    page.add(Row(
        controls=[
            MenuBar([SubmenuButton(
                content=Text("New"),
                leading=Icon(icons.ADD),
                on_focus=lambda e: print(e),
                controls=[
                    SubmenuButton(
                        content=Text("Function"),
                        leading=Icon(icons.FUNCTIONS),
                        controls=[
                            MenuItemButton(

                                on_hover=None,
                                content=Text("Function")
                            )
                        ]
                    ),
                    MenuItemButton(
                        content=Text("Equation"),
                        leading=Icon(icons.FUNCTIONS),
                        on_click=lambda e: print("add e"),
                        on_hover=None,
                    )
                ]
            )])
        ],
        alignment=MainAxisAlignment.END
    ))


app(main)
