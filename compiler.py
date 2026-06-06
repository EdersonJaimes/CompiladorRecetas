from lexer_ply import lexer
import parser_ply
from parser_ply import parser

class Compiler:

    def compilar(self, codigo):

        parser_ply.reiniciar_generador()

        lexer.input(codigo)

        tokens_generados = []

        while True:

            tok = lexer.token()

            if not tok:
                break

            tokens_generados.append(
                (
                    tok.type,
                    tok.value
                )
            )

        parser.parse(codigo)

        codigo_intermedio = (
            parser_ply.intermediate.obtener_codigo()
        )

        return (
            tokens_generados,
            codigo_intermedio
        )