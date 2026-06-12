class ASTNode:

    def __init__(self, nombre):

        self.nombre = nombre

        self.hijos = []

    def agregar(self, nodo):

        self.hijos.append(nodo)

        return nodo

    def a_texto(self, prefijo="", es_ultimo=True):
        """
        Devuelve una representación en árbol de texto, estilo:

        Programa
        ├── AGREGAR
        │   ├── HARINA
        │   ├── 250
        │   └── gr
        └── REPETIR
            ├── 5
            └── BATIR
        """

        lineas = []

        conector = "└── " if es_ultimo else "├── "
        lineas.append(prefijo + conector + self.nombre)

        extension = "    " if es_ultimo else "│   "
        nuevo_prefijo = prefijo + extension

        for i, hijo in enumerate(self.hijos):
            ultimo_hijo = (i == len(self.hijos) - 1)
            lineas.append(hijo.a_texto(nuevo_prefijo, ultimo_hijo))

        return "\n".join(lineas)

    def __str__(self):
        # Para la raíz, no queremos el conector inicial
        lineas = [self.nombre]
        for i, hijo in enumerate(self.hijos):
            ultimo_hijo = (i == len(self.hijos) - 1)
            lineas.append(hijo.a_texto("", ultimo_hijo))
        return "\n".join(lineas)
