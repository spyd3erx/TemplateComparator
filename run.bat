@echo off
setlocal enabledelayedexpansion

color 0A

echo ===================================================
echo   Verificando el entorno de Python
echo ===================================================

:: Verifica si python.exe esta disponible
python --version >nul 2>&1

if %errorlevel% neq 0 (
    echo [!] Python no esta instalado en el sistema.
    
    echo [*] Descargando e instalando el gestor de paquetes UV...
    powershell -ExecutionPolicy ByPass -Command "Invoke-RestMethod -Uri https://astral.sh/uv/install.ps1 | Invoke-Expression"
    
    :: Refresca el PATH temporalmente para poder usar 'uv' de inmediato en esta misma ventana
    set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"
    
    echo [*] Instalando Python 3.14 usando UV...
    uv python install 3.14
    
    echo [*] Instalando dependencias...
    if exist "pyproject.toml" (
        uv sync pyproject.toml
    ) else (
        echo [!] No se encontro un archivo "pyproject.toml". Se omitira la instalacion de dependencias.
    )
    
    echo [*] Ejecutando...
    if exist "main.py" (
        uv run main.py
    ) else (
        echo [!] Error: No se encontro el script "main.py" para ejecutar.
    )

) else (
    echo [*] Python ya esta instalado. Continuando con la ejecucion del script...
    
    echo [*] Ejecutando...
    if exist "main.py" (
        uv run main.py
    ) else (
        echo [!] Error: No se encontro el script "main.py" para ejecutar.
    )
)

echo ===================================================
echo   Proceso finalizado.
echo ===================================================