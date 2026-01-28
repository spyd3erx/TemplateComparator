import re
from typing import Any, Union

# Constantes
FORMULA_PREFIXES = ("=", "+", "-")
FORMULA_PATTERN = r'"(?:[^"]|"")*"|[^"\s]+'

def normalizar_formula(v: str) -> str:
    """Normaliza una fórmula de Excel."""
    if not isinstance(v, str):
        return v
    
    v = v.strip()
    
    if not _es_formula(v):
        return v
    
    v_limpio = _limpiar_prefijo(v)
    return _eliminar_caracteres_fijos(_eliminar_espacios_externos(v_limpio))

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