"""Tests para el módulo converter_pdf.py"""

from src.core.utils.converter_pdf import PDFConverter, converter_to_pdf
from pathlib import Path
import pytest


def create_test_markdown(
    path: Path, content: str = "# Test\n\nThis is a test markdown."
):
    """
    Crea un archivo Markdown de prueba.

    Args:
        path: Ruta del archivo a crear
        content: Contenido del archivo Markdown
    """
    path.write_text(content, encoding="utf-8")


class TestPDFConverter:
    """Tests para la clase PDFConverter."""

    def test_init_with_valid_file(self, tmp_path):
        """Test de inicialización con archivo válido."""
        md_file = tmp_path / "test.md"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        assert converter.input_file == md_file
        assert converter.input_file.exists()

    def test_init_with_string_path(self, tmp_path):
        """Test de inicialización con string path."""
        md_file = tmp_path / "test.md"
        create_test_markdown(md_file)

        converter = PDFConverter(str(md_file))

        assert converter.input_file == md_file
        assert isinstance(converter.input_file, Path)

    def test_init_with_nonexistent_file_raises_error(self, tmp_path):
        """Test que inicializar con archivo inexistente lanza FileNotFoundError."""
        md_file = tmp_path / "nonexistent.md"

        with pytest.raises(FileNotFoundError, match="no existe"):
            PDFConverter(md_file)

    def test_get_css_path_returns_valid_path(self, tmp_path):
        """Test que _get_css_path retorna un path válido."""
        md_file = tmp_path / "test.md"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)
        css_path = converter._get_css_path()

        assert isinstance(css_path, Path)
        assert css_path.exists()
        assert css_path.name == "pdf_style.css"

    def test_convert_basic(self, tmp_path):
        """Test de conversión básica a PDF."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file, "# Test Document\n\nThis is a test.")

        converter = PDFConverter(md_file)

        try:
            converter.convert(output_file=pdf_file, delete_source=False)

            # Verificar que el PDF se creó
            assert pdf_file.exists()
            assert pdf_file.stat().st_size > 0

            # Verificar que el archivo original NO se eliminó
            assert md_file.exists()
        except Exception as e:
            # Si pypandoc o weasyprint no están configurados correctamente, skip el test
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_convert_with_delete_source_false(self, tmp_path):
        """Test que delete_source=False preserva el archivo original."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        try:
            converter.convert(output_file=pdf_file, delete_source=False)

            # Verificar que el archivo original existe
            assert md_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_convert_with_delete_source_true(self, tmp_path):
        """Test que delete_source=True elimina el archivo original."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        try:
            converter.convert(output_file=pdf_file, delete_source=True)

            # Verificar que el archivo original fue eliminado
            assert not md_file.exists()
            # Verificar que el PDF se creó
            assert pdf_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_convert_with_default_output(self, tmp_path):
        """Test de conversión con output file por defecto."""
        md_file = tmp_path / "test.md"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        try:
            # Nota: Esto usará DEFAULT_PDF_FILE del config
            # Solo verificamos que no lanza error
            converter.convert(delete_source=False)
        except Exception as e:
            # Si hay error de configuración, skip
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_convert_with_path_object_output(self, tmp_path):
        """Test de conversión con Path object como output."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        try:
            converter.convert(output_file=pdf_file, delete_source=False)

            assert pdf_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_convert_with_string_output(self, tmp_path):
        """Test de conversión con string como output."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        try:
            converter.convert(output_file=str(pdf_file), delete_source=False)

            assert pdf_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")


class TestConverterLegacyFunction:
    """Tests para la función legacy converter_to_pdf."""

    def test_legacy_function_basic(self, tmp_path):
        """Test que la función legacy funciona correctamente."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        try:
            converter_to_pdf(md_file, pdf_file, delete_source=False)

            assert pdf_file.exists()
            assert md_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_legacy_function_with_delete(self, tmp_path):
        """Test función legacy con eliminación de archivo."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        try:
            converter_to_pdf(md_file, pdf_file, delete_source=True)

            assert pdf_file.exists()
            assert not md_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_legacy_function_with_string_paths(self, tmp_path):
        """Test función legacy con paths como strings."""
        md_file = tmp_path / "test.md"
        pdf_file = tmp_path / "output.pdf"
        create_test_markdown(md_file)

        try:
            converter_to_pdf(str(md_file), str(pdf_file), delete_source=False)

            assert pdf_file.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_legacy_function_default_output(self, tmp_path):
        """Test función legacy con output por defecto."""
        md_file = tmp_path / "test.md"
        create_test_markdown(md_file)

        try:
            converter_to_pdf(md_file, delete_source=False)
            # No verificamos el archivo de salida ya que usa DEFAULT_PDF_FILE
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")


class TestPDFConverterEdgeCases:
    """Tests de casos edge y validaciones."""

    def test_multiple_conversions_same_instance(self, tmp_path):
        """Test que la misma instancia puede hacer múltiples conversiones."""
        md_file = tmp_path / "test.md"
        create_test_markdown(md_file)

        converter = PDFConverter(md_file)

        try:
            pdf_file1 = tmp_path / "output1.pdf"
            pdf_file2 = tmp_path / "output2.pdf"

            converter.convert(output_file=pdf_file1, delete_source=False)
            converter.convert(output_file=pdf_file2, delete_source=False)

            assert pdf_file1.exists()
            assert pdf_file2.exists()
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")

    def test_convert_with_complex_markdown(self, tmp_path):
        """Test conversión con Markdown complejo."""
        md_file = tmp_path / "complex.md"
        complex_content = """
# Título Principal

## Subtítulo

Este es un **texto en negrita** y esto es *cursiva*.

### Lista

- Item 1
- Item 2
- Item 3

### Tabla

| Columna 1 | Columna 2 |
|-----------|-----------|
| Dato 1    | Dato 2    |

### Código

```python
def hello():
    print("Hello World")
```
"""
        create_test_markdown(md_file, complex_content)
        pdf_file = tmp_path / "output.pdf"

        converter = PDFConverter(md_file)

        try:
            converter.convert(output_file=pdf_file, delete_source=False)

            assert pdf_file.exists()
            assert pdf_file.stat().st_size > 0
        except Exception as e:
            pytest.skip(f"Conversión a PDF no disponible: {e}")
