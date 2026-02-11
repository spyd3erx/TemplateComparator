"""View for comparing Defined Names (Name Manager) between two Excel files."""

import flet as ft
import threading
from pathlib import Path

from src.gui import theme as t
from src.gui.widgets import (
    app_card,
    section_title,
    caption_text,
    primary_button,
    file_picker_field,
    status_badge,
)
from src.core.defined_name_comparison import DefinedNameComparison


class DefinedNamesView(ft.Column):
    """View for comparing defined names between two Excel files."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.main_page = page
        self.file1_path: str = ""
        self.file2_path: str = ""
        self.spacing = t.PADDING_MD
        self.expand = True

        # File pickers (services en Flet 0.80+)
        self._picker1 = ft.FilePicker()
        self._picker2 = ft.FilePicker()
        page.services.append(self._picker1)
        page.services.append(self._picker2)

        # Controls
        self._status_text = ft.Text("", size=t.CAPTION_SIZE, color=t.TEXT_SECONDARY)
        self._progress = ft.ProgressBar(
            visible=False, color=t.PRIMARY, bgcolor=t.BORDER
        )
        self._results_column = ft.Column(spacing=t.PADDING_SM, visible=False)

        self._run_button = primary_button(
            "Comparar nombres definidos",
            icon=ft.Icons.PLAYLIST_ADD_CHECK,
            on_click=self._on_compare,
            disabled=True,
            expand=True,
        )

        self._file1_field = file_picker_field(
            label="Archivo base (original)",
            value="",
            on_click=self._pick_file1,
        )
        self._file2_field = file_picker_field(
            label="Archivo a comparar",
            value="",
            on_click=self._pick_file2,
        )

        self._build_layout()

    def _build_layout(self):
        header = ft.Column(
            controls=[
                ft.Text(
                    "Comparar Nombres Definidos",
                    size=t.HEADING_SIZE,
                    weight=ft.FontWeight.W_700,
                    color=t.TEXT_PRIMARY,
                ),
                caption_text(
                    "Compara el Administrador de Nombres entre dos archivos Excel. Identifica coincidencias, diferencias y nombres exclusivos."
                ),
            ],
            spacing=4,
        )

        files_section = app_card(
            ft.Column(
                controls=[
                    section_title("Archivos"),
                    self._file1_field,
                    self._file2_field,
                ],
                spacing=t.PADDING_SM,
            )
        )

        actions_section = ft.Row(controls=[self._run_button])

        progress_section = ft.Column(
            controls=[self._progress, self._status_text],
            spacing=4,
        )

        results_section = app_card(
            ft.Column(
                controls=[
                    section_title("Resultados"),
                    self._results_column,
                ],
                spacing=t.PADDING_SM,
            )
        )

        self.controls = [
            header,
            files_section,
            actions_section,
            progress_section,
            results_section,
        ]

    # ── File Picker Callbacks ──

    async def _pick_file1(self, _):
        """Pick file 1 using async picker."""
        try:
            files = await self._picker1.pick_files(
                dialog_title="Seleccionar archivo Excel base",
                allowed_extensions=["xlsx", "xlsm"],
                file_type=ft.FilePickerFileType.CUSTOM,
            )
            if files:
                self.file1_path = files[0].path
                self._rebuild_file_field(1)
                self._update_run_button()
                self.main_page.update()
        except Exception as e:
            print(f"Error picking file 1: {e}")

    async def _pick_file2(self, _):
        """Pick file 2 using async picker."""
        try:
            files = await self._picker2.pick_files(
                dialog_title="Seleccionar archivo Excel a comparar",
                allowed_extensions=["xlsx", "xlsm"],
                file_type=ft.FilePickerFileType.CUSTOM,
            )
            if files:
                self.file2_path = files[0].path
                self._rebuild_file_field(2)
                self._update_run_button()
                self.main_page.update()
        except Exception as e:
            print(f"Error picking file 2: {e}")

    def _rebuild_file_field(self, index: int):
        path = self.file1_path if index == 1 else self.file2_path
        label = "Archivo base (original)" if index == 1 else "Archivo a comparar"

        new_field = file_picker_field(
            label=label,
            value=Path(path).name if path else "",
            on_click=self._pick_file1 if index == 1 else self._pick_file2,
        )

        if index == 1:
            self._file1_field = new_field
        else:
            self._file2_field = new_field

        files_section = app_card(
            ft.Column(
                controls=[
                    section_title("Archivos"),
                    self._file1_field,
                    self._file2_field,
                ],
                spacing=t.PADDING_SM,
            )
        )
        self.controls[1] = files_section

    def _update_run_button(self):
        self._run_button.disabled = not (self.file1_path and self.file2_path)

    # ── Compare ──

    def _on_compare(self, e):
        self._set_running(True, "Comparando nombres definidos...")
        self._results_column.controls.clear()
        self._results_column.visible = False
        self.main_page.update()

        def run():
            try:
                comparison = DefinedNameComparison(self.file1_path, self.file2_path)
                results = comparison.defined_names_diff()
                self._display_results(results)
                self._set_running(False, "Comparacion completada exitosamente.")
            except Exception as ex:
                self._set_running(False, f"Error: {ex}")
                self._results_column.controls = [
                    status_badge(str(ex), t.ERROR, ft.Icons.ERROR_OUTLINE)
                ]
                self._results_column.visible = True

            self._update_run_button()
            self.main_page.update()

        threading.Thread(target=run, daemon=True).start()

    def _display_results(self, results: dict):
        """Display comparison results organized by category."""
        controls = []

        # Summary badges
        counts = {
            "coincidencias": len(results.get("coincidencias", [])),
            "diferencias": len(results.get("diferencias", [])),
            "solo_en_archivo1": len(results.get("solo_en_archivo1", [])),
            "solo_en_archivo2": len(results.get("solo_en_archivo2", [])),
        }

        summary = ft.Row(
            controls=[
                status_badge(
                    f"{counts['coincidencias']} coincidencias",
                    t.SUCCESS,
                    ft.Icons.CHECK_CIRCLE_OUTLINE,
                ),
                status_badge(
                    f"{counts['diferencias']} diferencias",
                    t.ERROR,
                    ft.Icons.WARNING_AMBER_ROUNDED,
                ),
                status_badge(
                    f"{counts['solo_en_archivo1']} solo en base",
                    t.WARNING,
                    ft.Icons.ARROW_BACK,
                ),
                status_badge(
                    f"{counts['solo_en_archivo2']} solo en comparado",
                    t.WARNING,
                    ft.Icons.ARROW_FORWARD,
                ),
            ],
            wrap=True,
            spacing=8,
            run_spacing=8,
        )
        controls.append(summary)
        controls.append(ft.Divider(height=1, color=t.BORDER))

        # Differences table
        diffs = results.get("diferencias", [])
        if diffs:
            controls.append(self._build_diff_section("Diferencias", diffs, t.ERROR))

        # Only in file 1
        only1 = results.get("solo_en_archivo1", [])
        if only1:
            controls.append(
                self._build_only_section(
                    f"Solo en {Path(self.file1_path).stem}", only1, t.WARNING
                )
            )

        # Only in file 2
        only2 = results.get("solo_en_archivo2", [])
        if only2:
            controls.append(
                self._build_only_section(
                    f"Solo en {Path(self.file2_path).stem}", only2, t.WARNING
                )
            )

        # Matches (collapsed by default)
        matches = results.get("coincidencias", [])
        if matches:
            controls.append(
                self._build_only_section("Coincidencias", matches, t.SUCCESS)
            )

        self._results_column.controls = controls
        self._results_column.visible = True

    def _build_diff_section(self, title: str, items: list, color: str) -> ft.Column:
        """Build a section showing name differences."""
        file1_stem = Path(self.file1_path).stem
        file2_stem = Path(self.file2_path).stem

        rows = []
        for item in items[:200]:
            name = item.get("nombre", "")
            val1 = item.get(file1_stem, "")
            val2 = item.get(file2_stem, "")
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                name,
                                size=11,
                                weight=ft.FontWeight.W_600,
                                selectable=True,
                            )
                        ),
                        ft.DataCell(ft.Text(str(val1), size=11, selectable=True)),
                        ft.DataCell(ft.Text(str(val2), size=11, selectable=True)),
                    ]
                )
            )

        return ft.Column(
            controls=[
                ft.Text(
                    title, weight=ft.FontWeight.W_600, size=t.BODY_SIZE, color=color
                ),
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(
                                ft.Text(
                                    "Nombre",
                                    weight=ft.FontWeight.W_600,
                                    size=t.CAPTION_SIZE,
                                )
                            ),
                            ft.DataColumn(
                                ft.Text(
                                    file1_stem,
                                    weight=ft.FontWeight.W_600,
                                    size=t.CAPTION_SIZE,
                                )
                            ),
                            ft.DataColumn(
                                ft.Text(
                                    file2_stem,
                                    weight=ft.FontWeight.W_600,
                                    size=t.CAPTION_SIZE,
                                )
                            ),
                        ],
                        rows=rows,
                        border=ft.Border.all(1, t.BORDER),
                        border_radius=t.BUTTON_RADIUS,
                        heading_row_color=ft.Colors.with_opacity(0.04, color),
                        heading_row_height=40,
                        data_row_min_height=36,
                        column_spacing=t.PADDING_SM,
                        horizontal_margin=t.PADDING_SM,
                    ),
                    border_radius=t.BUTTON_RADIUS,
                ),
            ],
            spacing=6,
        )

    def _build_only_section(self, title: str, items: list, color: str) -> ft.Column:
        """Build a section for names only in one file or matches."""
        rows = []
        for item in items[:200]:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                item.get("nombre", ""),
                                size=11,
                                weight=ft.FontWeight.W_600,
                                selectable=True,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                str(item.get("valor", "")), size=11, selectable=True
                            )
                        ),
                    ]
                )
            )

        return ft.Column(
            controls=[
                ft.Text(
                    title, weight=ft.FontWeight.W_600, size=t.BODY_SIZE, color=color
                ),
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(
                                ft.Text(
                                    "Nombre",
                                    weight=ft.FontWeight.W_600,
                                    size=t.CAPTION_SIZE,
                                )
                            ),
                            ft.DataColumn(
                                ft.Text(
                                    "Valor",
                                    weight=ft.FontWeight.W_600,
                                    size=t.CAPTION_SIZE,
                                )
                            ),
                        ],
                        rows=rows,
                        border=ft.Border.all(1, t.BORDER),
                        border_radius=t.BUTTON_RADIUS,
                        heading_row_color=ft.Colors.with_opacity(0.04, color),
                        heading_row_height=40,
                        data_row_min_height=36,
                        column_spacing=t.PADDING_SM,
                        horizontal_margin=t.PADDING_SM,
                    ),
                    border_radius=t.BUTTON_RADIUS,
                ),
            ],
            spacing=6,
        )

    # ── Helpers ──

    def _set_running(self, running: bool, message: str):
        self._progress.visible = running
        self._status_text.value = message
        self._run_button.disabled = running
