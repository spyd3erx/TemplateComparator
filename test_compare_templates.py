from src.core.compare_templates import TemplateComparison
from pathlib import Path
import time


base_path = Path(__file__).parent

start = time.perf_counter()

TemplateComparison(
    base_path / "RV_Patrimonio_SAP.xlsm",
    base_path / "RV_Patrimonio_DIS.xlsx",
).compare(
    compare_values=False,
    output_md=base_path / "reporte.md",
)

elapsed = time.perf_counter() - start
print(f"Tiempo de comparación (solo core): {elapsed:.2f} s")