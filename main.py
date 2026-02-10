import flet as ft
from src.gui.app import TemplateComparatorApp


def main():
    """Launch the Template Comparator desktop application."""
    app = TemplateComparatorApp()
    ft.run(app.build)


if __name__ == "__main__":
    main()
