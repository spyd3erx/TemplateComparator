from src.core.compare_templates import TemplateComparison
from pathlib import Path


base_path = Path(__file__).parent

TemplateComparison(
    base_path / "RV_Patrimonio_SAP.xlsm",
    base_path / "RV_Patrimonio_DIS.xlsx",
).compare(
    compare_values=False,
    output_md=base_path / "reporte.md",
)