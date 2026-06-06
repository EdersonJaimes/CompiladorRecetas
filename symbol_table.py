class SymbolTable:

    def __init__(self):

        self.simbolos = {}

    def registrar(self, nombre, tipo):

        self.simbolos[nombre] = tipo

    def obtener_todos(self):

        return self.simbolos