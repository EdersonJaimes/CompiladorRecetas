class ASTNode:

    def __init__(self, nombre):

        self.nombre = nombre

        self.hijos = []

    def agregar(self, nodo):

        self.hijos.append(nodo)