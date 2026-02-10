import flet as ft
import asyncio


class MyView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page_ref = page
        self.picker = ft.FilePicker()
        # Adding to overlay in __init__
        self.page_ref.overlay.append(self.picker)

        self.controls = [
            ft.Text("Class-based View"),
            ft.FilledButton("Pick Files", on_click=self.pick),
        ]

    async def pick(self, e):
        print("Attempting to pick files...")
        try:
            # New async API
            res = await self.picker.pick_files(allow_multiple=True)
            print(f"Picked: {res}")
        except Exception as ex:
            print(f"Error picking: {ex}")


def main(page: ft.Page):
    print("App mounting")
    view = MyView(page)
    page.add(view)
    page.update()


if __name__ == "__main__":
    ft.run(main)
