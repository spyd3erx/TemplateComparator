"""View for comparing Excel templates (formulas and values)."""

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
from src.core.compare_templates import TemplateComparison
from src.core.utils.converter_pdf import PDFConverter
from src.config import REPORTS_PATH, DEFAULT_MARKDOWN_FILE


class CompareView(ft.Column):
    """Main comparison view for Excel templates."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.file1_path: str = ""
        self.file2_path: str = ""
        self.selected_sheet: str = ""
        self.compare_mode: str = "formulas"  # "formulas" or "values"
        self.spacing = t.PADDING_MD
        self.expand = True

        # File pickers
        self._picker1 = ft.FilePicker(on_result=self._on_file1_picked)
        self._picker2 = ft.FilePicker(on_result=self._on_file2_picked)
        page.overlay.extend([self._picker1, self._picker2])

        # Status and progress
        self._status_text = ft.Text("", size=t.CAPTION_SIZE, color=t.TEXT_SECONDARY)
        self._progress = ft.ProgressBar(visible=False, color=t.PRIMARY, bgcolor=t.BORDER)
        self._results_column = ft.Column(spacing=8, visible=False)
        self._run_button = primary_button(
            "Comparar plantillas",
            icon=ft.Icons.COMPARE_ARROWS,
            on_click=self._on_compare,
            disabled=True,
            expand=True,
        )
        self._export_button = primary_button(
            "Exportar PDF",
            icon=ft.Icons.PICTURE_AS_PDF_OUTLINED,
            on_click=self._on_export_pdf,
            disabled=True,
        )

        # File field refs
        self._file1_field = file_picker_field(
            label="Archivo base (original)",
            value=self.file1_path,
            on_click=lambda _: self._picker1.pick_files(
                dialog_title="Seleccionar archivo Excel base",
                allowed_extensions=["xlsx", "xlsm", "xls"],
                file_type=ft.FilePickerFileType.CUSTOM,
            ),
        )
        self._file2_field = file_picker_field(
            label="Archivo a comparar",
            value=self.file2_path,
            on_click=lambda _: self._picker2.pick_files(
                dialog_title="Seleccionar archivo Excel a comparar",
                allowed_extensions=["xlsx", "xlsm", "xls"],
                file_type=ft.FilePickerFileType.CUSTOM,
            ),
        )

        # Mode toggle
        self._mode_toggle = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(value="formulas", label="Comparar Formulas"),
                    ft.Radio(value="values", label="Comparar Valores"),
                ],
                spacing=t.PADDING_MD,
            ),
            value="formulas",
            on_change=self._on_mode_change,
        )

        # Sheet dropdown
        self._sheet_dropdown = ft.Dropdown(
            label="Hoja especifica (opcional)",
            hint_text="Todas las hojas comunes",
            border_color=t.BORDER,
            focused_border_color=t.PRIMARY,
            border_radius=t.BUTTON_RADIUS,
            text_size=t.BODY_SIZE,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
            on_change=self._on_sheet_change,
            expand=True,
        )

        self._build_layout()

    def _build_layout(self):
        """Constructs the full view layout."""
        header = ft.Column(
            controls=[
                ft.Text(
                    "Comparar Plantillas Excel",
                    size=t.HEADING_SIZE,
                    weight=ft.FontWeight.W_700,
                    color=t.TEXT_PRIMARY,
                ),
                caption_text(
                    "Selecciona dos archivos Excel para comparar sus formulas, valores o ambos."
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

        options_section = app_card(
            ft.Column(
                controls=[
                    section_title("Opciones de comparacion"),
                    self._mode_toggle,
                    self._sheet_dropdown,
                ],
                spacing=t.PADDING_SM,
            )
        )

        actions_section = ft.Row(
            controls=[self._run_button, self._export_button],
            spacing=t.PADDING_SM,
        )

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
            options_section,
            actions_section,
            progress_section,
            results_section,
        ]

    # ── File Picker Callbacks ──

    def _on_file1_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.file1_path = e.files[0].path
            self._rebuild_file_field(1)
            self._try_load_sheets()
            self._update_run_button()
            self.page.update()

    def _on_file2_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            self.file2_path = e.files[0].path
            self._rebuild_file_field(2)
            self._try_load_sheets()
            self._update_run_button()
            self.page.update()

    def _rebuild_file_field(self, index: int):
        """Rebuild the file field widget to reflect the new path."""
        path = self.file1_path if index == 1 else self.file2_path
        label = "Archivo base (original)" if index == 1 else "Archivo a comparar"
        picker = self._picker1 if index == 1 else self._picker2

        new_field = file_picker_field(
            label=label,
            value=Path(path).name if path else "",
            on_click=lambda _, p=picker: p.pick_files(
                dialog_title=f"Seleccionar archivo Excel",
                allowed_extensions=["xlsx", "xlsm", "xls"],
                file_type=ft.FilePickerFileType.CUSTOM,
            ),
        )

        if index == 1:
            self._file1_field = new_field
        else:
            self._file2_field = new_field

        # Rebuild files section in controls
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

    def _try_load_sheets(self):
        """Load common sheet names when both files are selected."""
        if not self.file1_path or not self.file2_path:
            return

        try:
            from src.core.utils.load_workbook import LoadWorkbook

            with LoadWorkbook(self.file1_path, only_read=True, only_data=True) as wb1:
                sheets1 = set(wb1.get_sheet_names())
            with LoadWorkbook(self.file2_path, only_read=True, only_data=True) as wb2:
                sheets2 = set(wb2.get_sheet_names())

            common = sorted(sheets1 & sheets2)
            self._sheet_dropdown.options = [ft.dropdown.Option(s) for s in common]
            self._sheet_dropdown.value = None
            self.selected_sheet = ""
        except Exception:
            self._sheet_dropdown.options = []

    def _on_mode_change(self, e):
        self.compare_mode = e.control.value

    def _on_sheet_change(self, e):
        self.selected_sheet = e.control.value or ""

    def _update_run_button(self):
        self._run_button.disabled = not (self.file1_path and self.file2_path)

    # ── Compare Logic ──

    def _on_compare(self, e):
        """Runs the comparison in a background thread."""
        self._set_running(True, "Comparando archivos...")
        self._results_column.controls.clear()
        self._results_column.visible = False
        self._export_button.disabled = True
        self.page.update()

        def run():
            try:
                compare_values = self.compare_mode == "values"
                sheet = self.selected_sheet or None

                REPORTS_PATH.mkdir(parents=True, exist_ok=True)
                md_path = str(REPORTS_PATH / DEFAULT_MARKDOWN_FILE)

                comparison = TemplateComparison(self.file1_path, self.file2_path)
                comparison.compare(compare_values, sheet, md_path)

                # Read back results to show in GUI
                md_content = Path(md_path).read_text(encoding="utf-8")
                self._display_results(md_content)
                self._set_running(False, "Comparacion completada exitosamente.")
                self._export_button.disabled = False

            except Exception as ex:
                self._set_running(False, f"Error: {ex}")
                self._results_column.controls = [
                    status_badge(str(ex), t.ERROR, ft.Icons.ERROR_OUTLINE)
                ]
                self._results_column.visible = True

            self.page.update()

        threading.Thread(target=run, daemon=True).start()

    def _display_results(self, md_content: str):
        """Parse markdown content and display in a data table."""
        lines = md_content.strip().split("\n")
        controls = []
        current_sheet = ""
        table_rows = []
        header_cols = []

        for line in lines:
            line = line.strip()
            if not line:
                if table_rows and current_sheet:
                    controls.append(self._build_result_table(current_sheet, header_cols, table_rows))
                    table_rows = []
                    header_cols = []
                continue

            if line.startswith("## Hoja:"):
                if table_rows and current_sheet:
                    controls.append(self._build_result_table(current_sheet, header_cols, table_rows))
                    table_rows = []
                    header_cols = []
                current_sheet = line.replace("## Hoja:", "").strip()

            elif line.startswith("Sin diferencias."):
                controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=t.SUCCESS, size=18),
                                ft.Text(
                                    f"Hoja: {current_sheet} - Sin diferencias",
                                    color=t.SUCCESS,
                                    weight=ft.FontWeight.W_600,
                                    size=t.BODY_SIZE,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=ft.padding.symmetric(vertical=6),
                    )
                )

            elif line.startswith("|") and "---" not in line:
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if not header_cols:
                    header_cols = cells
                else:
                    table_rows.append(cells)

        # Final flush
        if table_rows and current_sheet:
            controls.append(self._build_result_table(current_sheet, header_cols, table_rows))

        if not controls:
            controls.append(
                status_badge("Sin resultados para mostrar", t.WARNING, ft.Icons.INFO_OUTLINE)
            )

        self._results_column.controls = controls
        self._results_column.visible = True

    def _build_result_table(self, sheet_name: str, headers: list, rows: list) -> ft.Column:
        """Creates a DataTable for one sheet's differences."""
        diff_count = len(rows)
        color = t.ERROR if diff_count > 0 else t.SUCCESS

        columns = [
            ft.DataColumn(ft.Text(h, weight=ft.FontWeight.W_600, size=t.CAPTION_SIZE))
            for h in headers
        ]

        data_rows = []
        for row in rows[:200]:  # Limit to 200 rows for performance
            data_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(
                                cell.strip("`"),
                                size=11,
                                no_wrap=False,
                                selectable=True,
                            )
                        )
                        for cell in row
                    ]
                )
            )

        badge = status_badge(
            f"{diff_count} diferencia{'s' if diff_count != 1 else ''}",
            color,
            ft.Icons.WARNING_AMBER_ROUNDED if diff_count > 0 else ft.Icons.CHECK_CIRCLE_OUTLINE,
        )

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(f"Hoja: {sheet_name}", weight=ft.FontWeight.W_600, size=t.BODY_SIZE, color=t.TEXT_PRIMARY),
                        badge,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.DataTable(
                        columns=columns,
                        rows=data_rows,
                        border=ft.border.all(1, t.BORDER),
                        border_radius=t.BUTTON_RADIUS,
                        heading_row_color=ft.Colors.with_opacity(0.04, t.PRIMARY),
                        heading_row_height=40,
                        data_row_min_height=36,
                        column_spacing=t.PADDING_SM,
                        horizontal_margin=t.PADDING_SM,
                    ),
                    border_radius=t.BUTTON_RADIUS,
                ),
                ft.Divider(height=1, color=t.BORDER),
            ],
            spacing=8,
        )

    # ── Export PDF ──

    def _on_export_pdf(self, e):
        """Exports the markdown report to PDF."""
        self._set_running(True, "Generando PDF...")
        self.page.update()

        def run():
            try:
                md_path = REPORTS_PATH / DEFAULT_MARKDOWN_FILE
                pdf_path = REPORTS_PATH / "reporte_final.pdf"

                converter = PDFConverter(md_path)
                converter.convert(pdf_path, delete_source=False)

                self._set_running(False, f"PDF exportado en: {pdf_path}")
            except Exception as ex:
                self._set_running(False, f"Error al exportar PDF: {ex}")

            self.page.update()

        threading.Thread(target=run, daemon=True).start()

    # ── Helpers ──

    def _set_running(self, running: bool, message: str):
        self._progress.visible = running
        self._status_text.value = message
        self._run_button.disabled = running
