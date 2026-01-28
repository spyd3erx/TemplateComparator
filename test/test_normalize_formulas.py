from src.core.utils.normalize_formulas import normalizar


class TestEsFormula:
    
    def test_es_formula_igual(self):
        assert normalizar("=SUM(A1:A10)") == "=SUM(A1:A10)"

    def test_es_formula_mas(self):
        assert normalizar("+=5") == '=5'

    def test_es_formula_menos(self):
        assert normalizar("-5") == '=-5'

    def test_no_es_formula(self):
        assert normalizar("4434353-PyG") == "4434353-PyG"

    def test_no_es_formula_vacia(self):
        assert normalizar("") == 0


class TestLimpiarPrefijo:
    def test_limpiar_prefijo_igual(self):
        assert normalizar("=SUM(A1)") == "=SUM(A1)"

    def test_limpiar_prefijo_mas(self):
        assert normalizar("+5") == "=5"

    def test_limpiar_prefijo_menos(self):
        assert normalizar("-3") == "=-3"

    def test_limpiar_prefijo_multiples(self):
        assert normalizar("==$A$1") == "=A1"


class TestEliminarEspaciosExternos:
    def test_eliminar_espacios_simples(self):
        assert normalizar("= SUM ( A1 )") == "=SUM(A1)"

    def test_preservar_espacios_entrecomillados(self):
        assert (
            normalizar('= "texto con espacios"')
            == '="texto con espacios"'
        )

    def test_sin_espacios(self):
        assert normalizar("=SUM(A1)") == "=SUM(A1)"


class TestNormalizarFormula:
    def test_normalizar_formula_basica(self):
        assert normalizar("= SUM ( A1 : A10 )") == "=SUM(A1:A10)"

    def test_normalizar_formula_con_prefijo_mas(self):
        assert normalizar("+ 5") == "=5"

    def test_normalizar_formula_con_prefijo_menos(self):
        assert normalizar("- 3") == "=-3"

    def test_normalizar_no_formula(self):
        assert normalizar("texto normal") == "texto normal"

    def test_normalizar_con_espacios(self):
        assert normalizar("  =A1  ") == "=A1"

    def test_normalizar_no_string(self):
        assert normalizar(123) == 123

    def test_normalizar_formula_entrecomillada(self):
        assert normalizar('= "texto" & A1') == '="texto"&A1'

    def test_normalizar_formula_con_valores_fijos(self):
        assert normalizar('= $A$1 +  10 ') == '=A1+10'
        assert normalizar('=  B2  *  $C$3 ') == '=B2*C3'


class TestNormalizar:
    """Tests para normalizar() - función universal que agrupa todas las normalizaciones."""
    
    def test_normalizar_none(self):
        assert normalizar(None) == 0

    def test_normalizar_string_vacio(self):
        assert normalizar("") == 0

    def test_normalizar_string_espacios(self):
        assert normalizar("   ") == 0

    def test_normalizar_string_valido(self):
        assert normalizar("texto") == "texto"

    def test_normalizar_numero(self):
        assert normalizar(42) == 42

    def test_normalizar_float(self):
        assert normalizar(3.14) == 3.14

    def test_normalizar_string_con_espacios(self):
        assert normalizar("  contenido  ") == "contenido"
    
    # Nuevos tests: normalizar() debe aplicar normalizar_formula() a fórmulas
    def test_normalizar_formula_simple(self):
        """normalizar() aplica normalizar_formula() detectando ="""
        assert normalizar("= SUM ( A1 : A10 )") == "=SUM(A1:A10)"
    
    def test_normalizar_formula_con_prefijo_mas(self):
        """normalizar() normaliza fórmulas con prefijo +"""
        assert normalizar("+ 5") == "=5"
    
    def test_normalizar_formula_con_prefijo_menos(self):
        """normalizar() normaliza fórmulas con prefijo -"""
        assert normalizar("- 3") == "=-3"
    
    def test_normalizar_formula_entrecomillada(self):
        """normalizar() preserva espacios dentro de comillas en fórmulas"""
        assert normalizar('= "texto con espacios" & A1') == '="texto con espacios"&A1'
    
    def test_normalizar_no_confunde_texto_con_formula(self):
        """normalizar() NO trata como fórmula si no empieza con =, +, -"""
        assert normalizar("  esto no es formula  ") == "esto no es formula"
    
    def test_normalizar_bool(self):
        """normalizar() mantiene booleanos sin cambios"""
        assert normalizar(True) is True
        assert normalizar(False) is False

class TestIntegracion:
    """Tests de integración que validan el flujo completo con normalizar()."""
    
    def test_integracion_formula_con_espacios(self):
        assert normalizar("  =  A1 + B2  ") == "=A1+B2"

    def test_integracion_celda_excel_formula_compleja(self):
        assert normalizar("= SUM ( A1 : A10 )") == "=SUM(A1:A10)"

    def test_integracion_celda_excel_numero(self):
        assert normalizar(42) == 42

    def test_integracion_celda_excel_texto(self):
        assert normalizar("  contenido de celda  ") == "contenido de celda"

    def test_integracion_celda_excel_vacia(self):
        assert normalizar("") == 0

    def test_integracion_formula_concatenacion(self):
        assert normalizar('= "Hola" & A1') == '="Hola"&A1'

    def test_integracion_formula_negativa(self):
        assert normalizar("- 5") == "=-5"
