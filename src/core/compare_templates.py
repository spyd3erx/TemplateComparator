from .utils.load_workbook import LoadWorkbook
from .utils.normalize_formulas import normalizar_formula, normalizar
from src.config import DEFAULT_MARKDOWN_FILE, EXCLUDE_PARAMS
from pathlib import Path
from openpyxl.worksheet.worksheet import Worksheet
from typing import Optional


class TemplateComparison:
    """Clase para comparar dos archivos de Excel (plantillas)."""

    def __init__(self, path1: Path, path2: Path):
        """
        Inicializa la comparación entre dos archivos Excel.

        Args:
            path1: Ruta del primer archivo Excel
            path2: Ruta del segundo archivo Excel
        """
        self.path1 = Path(path1)
        self.path2 = Path(path2)

    def compare(
        self,
        compare_values: bool,
        sheet: Optional[str] = None,
        output_md: str = DEFAULT_MARKDOWN_FILE,
    ) -> None:
        """
        Compara dos archivos Excel y genera un reporte en Markdown.

        Args:
            compare_values: True para comparar valores, False para comparar fórmulas
            sheet: Nombre de la hoja específica a comparar (opcional)
            output_md: Ruta del archivo Markdown de salida
        """
        # compare_values=True -> data_only=True (Read Values)
        # compare_values=False -> data_only=False (Read Formulas)

        with LoadWorkbook(
            self.path1, only_read=True, only_data=compare_values
        ) as wb1_obj:
            with LoadWorkbook(
                self.path2, only_read=True, only_data=compare_values
            ) as wb2_obj:
                wb1 = wb1_obj.workbook
                wb2 = wb2_obj.workbook

                hojas1 = set(wb1.sheetnames)
                hojas2 = set(wb2.sheetnames)

                hojas_comunes = hojas1.intersection(hojas2)

                # Filter excluded sheets
                hojas_comunes = {h for h in hojas_comunes if h not in EXCLUDE_PARAMS}

                # Si no hay hojas en común después del filtrado, generamos igualmente
                # un reporte Markdown informativo en lugar de salir silenciosamente.
                if not hojas_comunes:
                    reporte_md = [
                        "# Reporte de comparación de plantillas",
                        "",
                        "No se encontraron hojas en común entre los archivos seleccionados ",
                        "después de aplicar los filtros de exclusión configurados.",
                        "",
                        f"- Archivo 1: `{self.path1.name}`",
                        f"- Archivo 2: `{self.path2.name}`",
                        "",
                    ]
                    self._save_report(output_md, reporte_md)
                    print(f"Reporte generado en: {output_md}")
                    return

                if sheet:
                    if sheet not in hojas_comunes:
                        raise ValueError(
                            f"La hoja '{sheet}' no existe en ambos archivos."
                        )
                    hojas_a_comparar = {sheet}
                else:
                    hojas_a_comparar = hojas_comunes

                reporte_md = self._generate_report(
                    wb1, wb2, hojas_a_comparar, compare_values
                )

        # Guardar archivo MD
        self._save_report(output_md, reporte_md)
        print(f"Reporte generado en: {output_md}")

    def _generate_report(
        self, wb1, wb2, hojas_a_comparar: set[str], compare_values: bool
    ) -> list[str]:
        """
        Genera el reporte completo comparando todas las hojas seleccionadas.

        Args:
            wb1: Primer workbook
            wb2: Segundo workbook
            hojas_a_comparar: Set de nombres de hojas a comparar
            compare_values: True para valores, False para fórmulas

        Returns:
            Lista de líneas del reporte en Markdown
        """
        archivo1_nombre = self.path1.stem
        archivo2_nombre = self.path2.stem
        reporte_md = []

        for hoja in sorted(hojas_a_comparar):
            ws1: Worksheet = wb1[hoja]
            ws2: Worksheet = wb2[hoja]

            diferencias = self._compare_sheets(ws1, ws2, compare_values)

            # Construcción de tabla Markdown
            reporte_md.append(f"## Hoja: {hoja}\n")

            if diferencias:
                reporte_md.append(f"| Celda | {archivo1_nombre} | {archivo2_nombre} |")
                reporte_md.append("|-------|-----------|-----------|")

                for d in diferencias:
                    v1_str = str(d["archivo1"]).replace("|", "\\|")
                    v2_str = str(d["archivo2"]).replace("|", "\\|")
                    reporte_md.append(f"| {d['celda']} | `{v1_str}` | `{v2_str}` |")
            else:
                reporte_md.append("Sin diferencias.\n")

            reporte_md.append("\n")

        return reporte_md

    def _compare_sheets(
        self, ws1: Worksheet, ws2: Worksheet, compare_values: bool
    ) -> list[dict]:
        """
        Compara dos hojas de Excel y devuelve las diferencias.

        Args:
            ws1: Primera hoja
            ws2: Segunda hoja
            compare_values: True para valores, False para fórmulas

        Returns:
            Lista de diferencias encontradas
        """
        # Calculate max bounds to iterate efficiently
        max_row = max(ws1.max_row, ws2.max_row)
        max_col = max(ws1.max_column, ws2.max_column)

        diferencias = []

        for row in range(1, max_row + 1):
            for col in range(1, max_col + 1):
                c1 = ws1.cell(row=row, column=col)
                c2 = ws2.cell(row=row, column=col)

                v1_raw = c1.value
                v2_raw = c2.value

                # Filter: If in Formula Mode (compare_values=False),
                # skip comparison if neither cell has a formula (both are static values).
                if not compare_values:
                    if not self._should_compare_cell(v1_raw, v2_raw):
                        continue

                # Apply formula normalization always
                v1 = normalizar_formula(v1_raw)
                v2 = normalizar_formula(v2_raw)

                v1 = normalizar(v1)
                v2 = normalizar(v2)

                if v1 != v2:
                    diferencias.append(
                        {"celda": c1.coordinate, "archivo1": v1, "archivo2": v2}
                    )

        return diferencias

    def _should_compare_cell(self, v1_raw, v2_raw) -> bool:
        """
        Determina si una celda debe ser comparada en modo fórmulas.

        Args:
            v1_raw: Valor crudo de la celda 1
            v2_raw: Valor crudo de la celda 2

        Returns:
            True si la celda debe compararse, False si debe saltarse
        """
        # We consider it a formula if it is a string starting with '='
        is_f1 = isinstance(v1_raw, str) and v1_raw.strip().startswith("=")
        is_f2 = isinstance(v2_raw, str) and v2_raw.strip().startswith("=")

        # Extra requirement: "Evaluated cells contain only formulas"
        # Interpretation: Filter out noise where both are static.
        # We keep the case where one is formula and other is value (overwrite detection).
        if not is_f1 and not is_f2:
            return False

        return True

    def _save_report(self, output_path: str, content: list[str]) -> None:
        """
        Guarda el reporte en un archivo Markdown.

        Args:
            output_path: Ruta del archivo de salida
            content: Lista de líneas del reporte
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))


# Función de compatibilidad para mantener la interfaz anterior
def comparar_excels_md(
    archivo1: Path,
    archivo2: Path,
    compare_values: bool,
    sheet: Optional[str] = None,
    salida_md: str = DEFAULT_MARKDOWN_FILE,
) -> None:
    """
    Función legacy para compatibilidad con código existente.

    Args:
        archivo1: Ruta del primer archivo Excel
        archivo2: Ruta del segundo archivo Excel
        compare_values: True para comparar valores, False para comparar fórmulas
        sheet: Nombre de la hoja específica a comparar (opcional)
        salida_md: Ruta del archivo Markdown de salida
    """
    comparison = TemplateComparison(archivo1, archivo2)
    comparison.compare(compare_values, sheet, salida_md)
