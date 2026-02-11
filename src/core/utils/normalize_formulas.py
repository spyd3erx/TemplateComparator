import re
from typing import Any, Union

# Constantes
FORMULA_PREFIXES = ("=", "+", "-")
FORMULA_PATTERN = r'"(?:[^"]|"")*"|[^"\s]+'

def normalizar_formula(v: str) -> str:
    """
    Normaliza una fórmula de Excel (optimizada para rendimiento).
    Coincide con la lógica de la versión preliminar.
    """
    if not isinstance(v, str):
        return v
    
    v = v.strip()
    
    # Verificar si es fórmula (empieza con =, +, -)
    if not (v.startswith("=") or v.startswith("+") or v.startswith("-")):
        return v

    # Estandarizar prefijo: '+IF' -> '=IF', '=+IF' -> '=IF', '=-IF' -> '=-IF'
    temp_v = v
    if temp_v.startswith("="):
        temp_v = temp_v[1:]
    if temp_v.startswith("+"):
        temp_v = temp_v[1:]
    v_clean = "=" + temp_v

    # Eliminar espacios fuera de cadenas entrecomilladas (regex optimizado)
    return "".join(re.findall(FORMULA_PATTERN, v_clean))

def _eliminar_caracteres_fijos(v: str) -> str:
    """Elimina los caracteres de referencia absoluta ($) de la fórmula."""
    return v.replace("$", "")

def _es_formula(v: str) -> bool:
    """Verifica si la cadena parece ser una fórmula."""
    return v.startswith(FORMULA_PREFIXES)

def _limpiar_prefijo(v: str) -> str:
    """Estandariza el prefijo de la fórmula."""
    # Remove leading formula characters
    stripped = v.lstrip("=+-")
    # Preserve leading minus sign if present
    if v.startswith("-") and not stripped.startswith("-"):
        stripped = "-" + stripped
    return f"={stripped}" if stripped else "=0"

def _eliminar_espacios_externos(v: str) -> str:
    """Elimina espacios fuera de cadenas entrecomilladas."""
    return "".join(re.findall(FORMULA_PATTERN, v))

def normalizar(v: Any) -> Union[int, str, Any]:
    """
    Normaliza cualquier valor aplicando todas las normalizaciones necesarias.
    
    Lógica:
    - None → 0
    - String vacío o espacios → 0
    - Fórmula Excel → aplica normalizar_formula()
    - String → retorna el string limpio
    - Otros → retorna sin cambios
    """
    if v is None:
        return 0
    
    if isinstance(v, str):
        v = v.strip()
        
        if not v:  # String vacío después de limpiar
            return 0
        
        if _es_formula(v):  # Si es fórmula, aplicar normalización específica
            return normalizar_formula(v)
        
        return v  # String normal limpio
    
    return v  # Otros tipos (números, bool, etc.)