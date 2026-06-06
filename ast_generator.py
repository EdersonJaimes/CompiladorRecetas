from graphviz import Digraph


class ASTGenerator:

    def __init__(self):

        self.dot = Digraph()

        self.contador = 0

    def generar(self, nodo):

        actual = str(self.contador)

        self.contador += 1

        self.dot.node(
            actual,
            nodo.nombre
        )

        for hijo in nodo.hijos:

            hijo_id = self.generar(hijo)

            self.dot.edge(
                actual,
                hijo_id
            )

        return actual

    def guardar(self, raiz):

        self.generar(raiz)

        self.dot.render(
            "arbol_sintactico",
            format="png",
            cleanup=True
        )