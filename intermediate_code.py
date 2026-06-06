class IntermediateCodeGenerator:

    def __init__(self):

        self.codigo = []

        self.label = 0

    def nuevo_label(self):

        self.label += 1

        return f"L{self.label}"

    def agregar(
        self,
        ingrediente,
        cantidad,
        unidad
    ):

        self.codigo.append(
            f"LOAD {ingrediente}, {cantidad} {unidad}"
        )

    def precalentar(
        self,
        temperatura
    ):

        self.codigo.append(
            f"SET TEMPERATURA {temperatura}"
        )

    def repetir(
        self,
        veces,
        accion
    ):

        L = self.nuevo_label()

        self.codigo.append(
            "TEMP_CONTADOR = 0"
        )

        self.codigo.append(
            f"LABEL {L}"
        )

        self.codigo.append(
            f"CALL {accion}"
        )

        self.codigo.append(
            "TEMP_CONTADOR = TEMP_CONTADOR + 1"
        )

        self.codigo.append(
            f"IF TEMP_CONTADOR < {veces} GOTO {L}"
        )

    def asignacion(
        self,
        variable,
        valor
    ):

        self.codigo.append(
            f"{variable} = {valor}"
        )

    def obtener_codigo(self):

        return "\n".join(
            self.codigo
        )