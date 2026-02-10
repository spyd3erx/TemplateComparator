import flet as ft
import asyncio


async def main(page: ft.Page):
    print("App started")

    picker = ft.FilePicker()
    page.overlay.append(picker)
    page.update()

    async def pick_files_click(_):
        print("Picking files...")
        try:
            files = await picker.pick_files(allow_multiple=True)
            print("Files picked:", files)
            if files:
                result_text.value = f"Selected: {[f.name for f in files]}"
                page.update()
        except Exception as e:
            print(f"Error picking files: {e}")

    result_text = ft.Text("No files picked")

    page.add(
        ft.FilledButton(
            "Pick files",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=pick_files_click,
        ),
        result_text,
    )


ft.run(main)
