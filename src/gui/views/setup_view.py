"""View for installing required dependencies (GTK Runtime and Pandoc)."""

import flet as ft
import threading

from src.gui import theme as t
from src.gui.widgets import app_card, section_title, caption_text, primary_button, status_badge


class SetupView(ft.Column):
    """View for installing required software dependencies."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.spacing = t.PADDING_MD
        self.expand = True

        self._status_text = ft.Text("", size=t.CAPTION_SIZE, color=t.TEXT_SECONDARY)
        self._progress = ft.ProgressBar(visible=False, color=t.PRIMARY, bgcolor=t.BORDER)
        self._log_column = ft.Column(spacing=4)

        self._install_button = primary_button(
            "Instalar dependencias",
            icon=ft.Icons.DOWNLOAD_OUTLINED,
            on_click=self._on_install,
        )

        self._build_layout()

    def _build_layout(self):
        header = ft.Column(
            controls=[
                ft.Text(
                    "Configuracion inicial",
                    size=t.HEADING_SIZE,
                    weight=ft.FontWeight.W_700,
                    color=t.TEXT_PRIMARY,
                ),
                caption_text(
                    "Instala las dependencias necesarias para la conversion de reportes a PDF."
                ),
            ],
            spacing=4,
        )

        info_section = app_card(
            ft.Column(
                controls=[
                    section_title("Dependencias requeridas"),
                    self._dep_item(
                        "GTK3 Runtime",
                        "Necesario para WeasyPrint (motor de renderizado PDF).",
                        ft.Icons.WINDOW_OUTLINED,
                    ),
                    self._dep_item(
                        "Pandoc",
                        "Conversor universal de documentos Markdown a PDF.",
                        ft.Icons.TRANSFORM_OUTLINED,
                    ),
                    ft.Divider(height=1, color=t.BORDER),
                    caption_text(
                        "Los archivos se descargaran en la carpeta Descargas. "
                        "GTK Runtime requiere instalacion manual."
                    ),
                ],
                spacing=t.PADDING_SM,
            )
        )

        actions_section = ft.Row(controls=[self._install_button])

        progress_section = ft.Column(
            controls=[self._progress, self._status_text],
            spacing=4,
        )

        log_section = app_card(
            ft.Column(
                controls=[
                    section_title("Registro"),
                    self._log_column,
                ],
                spacing=t.PADDING_SM,
            )
        )

        self.controls = [header, info_section, actions_section, progress_section, log_section]

    def _dep_item(self, name: str, description: str, icon: str) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, color=t.PRIMARY, size=22),
                    bgcolor=ft.Colors.with_opacity(0.08, t.PRIMARY),
                    border_radius=8,
                    padding=10,
                ),
                ft.Column(
                    controls=[
                        ft.Text(name, size=t.BODY_SIZE, weight=ft.FontWeight.W_600, color=t.TEXT_PRIMARY),
                        ft.Text(description, size=t.CAPTION_SIZE, color=t.TEXT_SECONDARY),
                    ],
                    spacing=2,
                    expand=True,
                ),
            ],
            spacing=t.PADDING_SM,
        )

    def _on_install(self, e):
        self._install_button.disabled = True
        self._progress.visible = True
        self._status_text.value = "Descargando dependencias..."
        self._log_column.controls.clear()
        self.page.update()

        def run():
            try:
                from src.core.utils.setup import setup_software

                self._add_log("Iniciando descarga de GTK Runtime y Pandoc...", t.PRIMARY)
                self.page.update()

                setup_software()

                self._add_log("Dependencias descargadas exitosamente.", t.SUCCESS)
                self._add_log(
                    "Recuerda instalar GTK Runtime manualmente desde la carpeta Descargas.",
                    t.WARNING,
                )
                self._status_text.value = "Instalacion completada."
            except Exception as ex:
                self._add_log(f"Error: {ex}", t.ERROR)
                self._status_text.value = f"Error durante la instalacion."

            self._progress.visible = False
            self._install_button.disabled = False
            self.page.update()

        threading.Thread(target=run, daemon=True).start()

    def _add_log(self, message: str, color: str):
        icon = ft.Icons.INFO_OUTLINE
        if color == t.SUCCESS:
            icon = ft.Icons.CHECK_CIRCLE_OUTLINE
        elif color == t.ERROR:
            icon = ft.Icons.ERROR_OUTLINE
        elif color == t.WARNING:
            icon = ft.Icons.WARNING_AMBER_ROUNDED

        self._log_column.controls.append(
            ft.Row(
                controls=[
                    ft.Icon(icon, size=14, color=color),
                    ft.Text(message, size=t.CAPTION_SIZE, color=color),
                ],
                spacing=6,
            )
        )
