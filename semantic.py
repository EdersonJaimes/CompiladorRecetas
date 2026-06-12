from symbols import INGREDIENTES, UNIDADES_VALIDAS
from errors import SemanticError
from symbol_table import SymbolTable


class SemanticAnalyzer:

    def __init__(self):

        self.tabla = SymbolTable()

    def validar_agregar(self, ingrediente, cantidad, unidad, linea=None):

        ingrediente_up = ingrediente.upper()

        if ingrediente_up not in INGREDIENTES:

            self.tabla.registrar(
                ingrediente_up,
                "INGREDIENTE_DESCONOCIDO",
                valor=f"{cantidad} {unidad}",
                linea=linea,
            )

            raise SemanticError(
                f"Ingrediente desconocido: {ingrediente_up}"
            )

        tipo = INGREDIENTES[ingrediente_up]

        unidad_correcta = UNIDADES_VALIDAS[tipo]

        self.tabla.registrar(
            ingrediente_up,
            f"INGREDIENTE_{tipo}",
            valor=f"{cantidad} {unidad}",
            linea=linea,
        )

        if unidad != unidad_correcta:

            raise SemanticError(
                f"{ingrediente_up} debe usar {unidad_correcta.lower()} "
                f"(se usó {unidad.lower()})"
            )

    def validar_temperatura(self, temperatura, linea=None):

        self.tabla.registrar(
            "TEMPERATURA",
            "PARAMETRO",
            valor=f"{temperatura} °C",
            linea=linea,
        )

        if temperatura < 50:

            raise SemanticError(
                "Temperatura demasiado baja (mínimo 50°C)"
            )

        if temperatura > 250:

            raise SemanticError(
                "Temperatura demasiado alta (máximo 250°C)"
            )

    def validar_cantidad(self, cantidad, linea=None):

        if cantidad <= 0:

            raise SemanticError(
                "Cantidad inválida (debe ser mayor a 0)"
            )

        if cantidad > 10000:

            raise SemanticError(
                "Cantidad excesiva (máximo 10000)"
            )

    def validar_repetir(self, veces, accion, linea=None):

        self.tabla.registrar(
            accion,
            "ACCION",
            valor=f"x{veces}",
            linea=linea,
        )

        if veces <= 0:

            raise SemanticError(
                "El número de repeticiones debe ser mayor a 0"
            )

        if veces > 100:

            raise SemanticError(
                "Número de repeticiones excesivo (máximo 100)"
            )

    def validar_asignacion(self, variable, valor, linea=None):

        self.tabla.registrar(
            variable,
            "VARIABLE",
            valor=valor,
            linea=linea,
        )
