import logging
import urllib.request
import shutil
from src.config import INSTALLERS_PATH

logger = logging.getLogger("template_validator")

def setup():
    logger.info("Iniciando configuración de dependencias...")

    # Crear carpeta de instaladores si no existe
    INSTALLERS_PATH.mkdir(parents=True, exist_ok=True)

    # GTK Runtime URL
    gtk_url = 'https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe'
    file_path = INSTALLERS_PATH / 'gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe'

    try:
        logger.info(f"Descargando GTK Runtime desde {gtk_url}...")
        
        # Download with urllib (Standard Lib)
        with urllib.request.urlopen(gtk_url) as response, open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        logger.info(f"Archivo descargado exitosamente en: {file_path}")
        logger.info("IMPORTANTE: Por favor instala el GTK Runtime manualmente para habilitar WeasyPrint.")

    except Exception as e:
        logger.error(f"Error durante la descarga de GTK: {e}")
        raise

