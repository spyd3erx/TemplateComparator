"""Módulo para convertir archivos Markdown a PDF usando Pandoc y WeasyPrint."""

import pypandoc
from pathlib import Path
from typing import Optional
from src.config import DEFAULT_PDF_FILE


class PDFConverter:
    """Clase para convertir archivos Markdown a PDF usando Pandoc y WeasyPrint."""

    def __init__(self, input_file: Path | str):
        """
        Inicializa el conversor con el archivo de entrada.

        Args:
            input_file: Ruta del archivo Markdown a convertir

        Raises:
            FileNotFoundError: Si el archivo de entrada no existe
        """
        self.input_file = Path(input_file)

        if not self.input_file.exists():
            raise FileNotFoundError(
                f"El archivo de entrada '{self.input_file}' no existe."
            )

    def convert(
        self, output_file: Optional[Path | str] = None, delete_source: bool = False
    ) -> None:
        """
        Convierte el archivo Markdown a PDF.

        Args:
            output_file: Ruta del archivo PDF de salida. Si es None, usa DEFAULT_PDF_FILE
            delete_source: Si True, elimina el archivo de entrada después de la conversión

        Raises:
            RuntimeError: Si la conversión falla
        """
        if output_file is None:
            output_file = DEFAULT_PDF_FILE

        output_path = Path(output_file)

        print(f"Iniciando conversión de {self.input_file} a PDF...")

        try:
            css_path = self._get_css_path()
            css_uri = css_path.as_uri()

            pypandoc.convert_file(
                str(self.input_file),
                "pdf",
                outputfile=str(output_path),
                extra_args=[
                    "--pdf-engine=weasyprint",
                    "--css",
                    css_uri,
                    "-V",
                    "geometry:margin=1cm",
                ],
            )

            print(f"Conversión exitosa: {output_path}")

            if delete_source and self.input_file.exists():
                self.input_file.unlink()
                print(f"Archivo original '{self.input_file}' eliminado.")

        except Exception as e:
            raise RuntimeError("Error durante la conversión a PDF")

        finally:
            print("Proceso de conversión finalizado")

    def _get_css_path(self) -> Path:
        """
        Obtiene la ruta del archivo CSS para styling del PDF.

        Returns:
            Path al archivo CSS

        Raises:
            FileNotFoundError: Si el archivo CSS no existe
        """
        css_path = Path(__file__).parent.parent.parent.parent / "assets" / "pdf_style.css"

        if not css_path.exists():
            raise FileNotFoundError(
                f"El archivo CSS '{css_path}' no existe. "
                "Asegúrate de tener 'pdf_style.css' en el directorio utils."
            )

        return css_path


# Función de compatibilidad para mantener la interfaz anterior
def converter_to_pdf(
    input_file: Path | str,
    output_file: Optional[Path | str] = None,
    delete_source: bool = False,
) -> None:
    """
    Función legacy para compatibilidad con código existente.

    Args:
        input_file: Ruta del archivo Markdown a convertir
        output_file: Ruta del archivo PDF de salida
        delete_source: Si True, elimina el archivo de entrada después de la conversión
    """
    converter = PDFConverter(input_file)
    converter.convert(output_file, delete_source)
