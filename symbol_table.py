class SymbolTable:

    def __init__(self):

        self.simbolos = {}

    def registrar(self, nombre, tipo, valor=None, linea=None):
        """
        Registra o actualiza un símbolo.

        nombre: nombre del símbolo (ingrediente o variable)
        tipo:   categoría (INGREDIENTE_LIQUIDO, INGREDIENTE_SOLIDO,
                INGREDIENTE_CONTABLE, VARIABLE, ACCION, etc.)
        valor:  información extra (cantidad+unidad, valor asignado, etc.)
        linea:  línea donde aparece (1-indexed)
        """

        if nombre not in self.simbolos:
            self.simbolos[nombre] = {
                "tipo": tipo,
                "valor": valor,
                "usos": [],
            }

        if valor is not None:
            self.simbolos[nombre]["valor"] = valor

        if linea is not None:
            self.simbolos[nombre]["usos"].append(linea)

    def obtener_todos(self):

        return self.simbolos

    def limpiar(self):

        self.simbolos = {}
