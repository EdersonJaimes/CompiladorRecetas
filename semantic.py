from symbols import *
from errors import SemanticError
from symbol_table import SymbolTable


class SemanticAnalyzer:

    def __init__(self):

        self.tabla = SymbolTable()

    def validar_agregar(self, ingrediente, unidad):
        self.tabla.registrar(
            ingrediente,
            unidad,
        )
    

        ingrediente = ingrediente.upper()

        if ingrediente not in INGREDIENTES:

            raise SemanticError(
                f"Ingrediente desconocido: {ingrediente}"
            )

        tipo = INGREDIENTES[ingrediente]

        unidad_correcta = UNIDADES_VALIDAS[tipo]

        if unidad != unidad_correcta:

            raise SemanticError(
                f"{ingrediente} debe usar {unidad_correcta}"
            )

    def validar_temperatura(
        self,
        temperatura
    ):

        if temperatura < 50:

            raise SemanticError(
                "Temperatura demasiado baja"
            )

        if temperatura > 250:

            raise SemanticError(
                "Temperatura demasiado alta"
            )

    def validar_cantidad(
        self,
        cantidad
    ):

        if cantidad <= 0:

            raise SemanticError(
                "Cantidad inválida"
            )

        if cantidad > 10000:

            raise SemanticError(
                "Cantidad excesiva"
            )