from openpyxl import load_workbook
from src.config import EXCLUDE_PARAMS


class LoadWorkbook:
    """
    Clase para cargar un archivo de excel.

    Args:
        file_path (str): Ruta del archivo de excel.

        only_read (bool): Indica si se debe cargar el archivo en modo de solo lectura. Default: True
        cuando se carga en este modo es necesario que se cierre el archivo explicitamente.

        only_data (bool): Indica si se debe cargar el archivo en modo de solo datos. Default: True
    """

    def __init__(self, file_path, only_read=True, only_data=True):
        """
        Inicializa la clase LoadWorkbook.
        """
        self.file_path = file_path
        self.workbook = load_workbook(
            file_path, read_only=only_read, data_only=only_data
        )

    def get_sheet_names(self):
        """
        Retorna los nombres de las hojas filtrando las excluidas.
        """
        exclude_set = set(EXCLUDE_PARAMS)

        return [name for name in self.workbook.sheetnames if name not in exclude_set]

    def get_sheet_by_name(self, sheet_name):
        """
        Obtiene una hoja del archivo de excel.

        Args:
            sheet_name (str): Nombre de la hoja.
        """
        return self.workbook[sheet_name]

    def close(self):
        """
        Cierra el archivo de excel.
        """
        self.workbook.close()
