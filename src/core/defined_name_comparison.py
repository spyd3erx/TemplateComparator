from .utils.load_workbook import LoadWorkbook
from .utils.recursive_ordering_dict import sort_complete_dict
from pathlib import Path


class DefinedNameComparison:
    """Clase para comparar los nombres definidos entre dos archivos de Excel."""

    def __init__(self, path1: Path, path2: Path):
        self.path1 = Path(path1)
        self.path2 = Path(path2)


    def get_defined_names(self, wb) -> dict:
        """Extrae todos los nombres definidos que NO están ocultos."""
        nombres_dict = dict()
        
        for name, property in wb.defined_names.items():
            if property.hidden:
                continue
                
            nombres_dict[str(name).upper()] = str(property.value)

        
        return sort_complete_dict(nombres_dict)


    def open_workbook(self, path: Path):
        """Abre un libro de Excel y devuelve el objeto workbook."""
        workbook = LoadWorkbook(path)
        return workbook

    def defined_names_diff(self) -> dict:
        """Compara los nombres definidos entre dos archivos de Excel."""
        file1 = self.path1
        file2 = self.path2
        wb1 = self.open_workbook(file1).workbook
        wb2 = self.open_workbook(file2).workbook

        admin_nombre_1: list[str] = self.get_defined_names(wb1)
        admin_nombre_2: list[str] = self.get_defined_names(wb2)

        comparativa = {
            "coincidencias": [],
            "diferencias": [],
            "solo_en_archivo1": [],
            "solo_en_archivo2": []
        }

        todos_los_nombres = set(admin_nombre_1.keys()) | set(admin_nombre_2.keys())

        for nombre in todos_los_nombres:
            val1 = admin_nombre_1.get(nombre)
            val2 = admin_nombre_2.get(nombre)

            if val1 == val2:
                comparativa["coincidencias"].append({"nombre": nombre, "valor": val1})
            elif val1 is not None and val2 is not None:
                comparativa["diferencias"].append({
                    "nombre": nombre, 
                    file1.stem: val1, 
                    file2.stem: val2
                })
            elif val1 is not None:
                comparativa["solo_en_archivo1"].append({"nombre": nombre, "valor": val1})
            else:
                comparativa["solo_en_archivo2"].append({"nombre": nombre, "valor": val2})
        wb1.close()
        wb2.close()
        return sort_complete_dict(comparativa) #sort_complete_dict() is only for test
