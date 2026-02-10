"""Main Flet application with sidebar navigation."""

import flet as ft
from . import theme as t
from .views.compare_view import CompareView
from .views.defined_names_view import DefinedNamesView
from .views.setup_view import SetupView


class TemplateComparatorApp:
    """Root application class managing navigation and views."""

    NAV_ITEMS = [
        {"label": "Comparar plantillas", "icon": ft.Icons.COMPARE_ARROWS, "index": 0},
        {"label": "Nombres definidos", "icon": ft.Icons.PLAYLIST_ADD_CHECK, "index": 1},
        {"label": "Configuracion", "icon": ft.Icons.SETTINGS_OUTLINED, "index": 2},
    ]

    def __init__(self):
        self._current_index = 0
        self._page: ft.Page | None = None
        self._content_area: ft.Column | None = None
        self._nav_rail: ft.NavigationRail | None = None
        self._views: dict[int, ft.Control] = {}

    def build(self, page: ft.Page):
        """Entry point called by flet.app()."""
        self._page = page
        page.title = "Template Comparator"
        page.window.width = 1100
        page.window.height = 750
        page.window.min_width = 860
        page.window.min_height = 600
        page.bgcolor = t.BACKGROUND
        page.theme = t.get_light_theme()
        page.padding = 0
        page.fonts = {"Segoe UI": ""}

        # Initialize views
        self._views = {
            0: CompareView(page),
            1: DefinedNamesView(page),
            2: SetupView(page),
        }

        # Navigation rail
        self._nav_rail = ft.NavigationRail(
            selected_index=self._current_index,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=80,
            min_extended_width=220,
            extended=True,
            bgcolor=t.SURFACE,
            indicator_color=ft.Colors.with_opacity(0.1, t.PRIMARY),
            on_change=self._on_nav_change,
            leading=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, color=t.SURFACE, size=24),
                            bgcolor=t.PRIMARY,
                            border_radius=10,
                            padding=10,
                        ),
                        ft.Text(
                            "Template\nComparator",
                            size=13,
                            weight=ft.FontWeight.W_700,
                            color=t.TEXT_PRIMARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
                padding=ft.padding.only(bottom=t.PADDING_MD),
            ),
            destinations=[
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(item["icon"], size=22),
                    selected_icon_content=ft.Icon(item["icon"], size=22, color=t.PRIMARY),
                    label=item["label"],
                )
                for item in self.NAV_ITEMS
            ],
        )

        # Content area (scrollable)
        self._content_area = ft.Column(
            controls=[self._views[self._current_index]],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # Layout: NavigationRail | Divider | Content
        page.add(
            ft.Row(
                controls=[
                    self._nav_rail,
                    ft.VerticalDivider(width=1, color=t.BORDER),
                    ft.Container(
                        content=self._content_area,
                        expand=True,
                        padding=t.PADDING_LG,
                    ),
                ],
                expand=True,
                spacing=0,
            )
        )

    def _on_nav_change(self, e):
        """Handle navigation rail selection change."""
        index = e.control.selected_index
        if index == self._current_index:
            return

        self._current_index = index
        self._content_area.controls = [self._views[index]]
        self._page.update()
