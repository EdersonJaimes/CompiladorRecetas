from lexer_ply import crear_lexer, LexicalErrorToken
import parser_ply
from parser_ply import parser
from ast_node import ASTNode
from errors import LexicalError, SyntaxCompilerError, SemanticError


class Compiler:

    def _dividir_en_instrucciones(self, codigo):
        """
        Divide el código fuente en "instrucciones", una por línea no
        vacía, conservando el número de línea (1-indexed).

        Devuelve una lista de tuplas (texto_instruccion, linea).
        """

        instrucciones = []

        for numero, linea in enumerate(codigo.splitlines(), start=1):

            texto = linea.strip()

            if not texto:
                continue

            instrucciones.append((texto, numero))

        return instrucciones

    def compilar(self, codigo):
        """
        Compila el código completo, recolectando TODOS los errores
        (léxicos, sintácticos y semánticos) en vez de detenerse en
        el primero.

        Devuelve un diccionario con:
            tokens:        lista de (tipo, valor) de TODO el código
            errores:       lista de strings "Línea N: mensaje"
            arbol:         ASTNode raíz ("Programa")
            tabla_simbolos: dict con la tabla de símbolos acumulada
            codigo_intermedio: string con el código intermedio generado
        """

        parser_ply.reiniciar_generador()

        instrucciones = self._dividir_en_instrucciones(codigo)

        tokens_generados = []
        errores = []

        raiz = ASTNode("Programa")

        for texto, linea in instrucciones:

            texto_strip = texto.strip()

            if not texto_strip:
                continue

            # ------------------------------------
            # ANÁLISIS LÉXICO de esta instrucción
            # ------------------------------------

            lx = crear_lexer()
            lx.input(texto_strip)

            tokens_instruccion = []
            error_lexico = None

            while True:
                try:
                    tok = lx.token()
                except LexicalErrorToken as e:
                    error_lexico = e
                    break

                if not tok:
                    break

                tokens_instruccion.append((tok.type, tok.value))
                tokens_generados.append((tok.type, tok.value))

            if error_lexico:
                errores.append(
                    f"Línea {linea}: ERROR LÉXICO: {error_lexico}"
                )
                # Aún así seguimos con la siguiente instrucción
                continue

            # Si la instrucción no termina en ';' es un error sintáctico
            if not texto_strip.endswith(";"):
                errores.append(
                    f"Línea {linea}: ERROR SINTÁCTICO: falta ';' al final de la instrucción"
                )
                continue

            # ------------------------------------
            # ANÁLISIS SINTÁCTICO + SEMÁNTICO
            # ------------------------------------

            parser_ply.set_linea_actual(linea)

            try:
                nodo = parser.parse(
                    texto_strip,
                    lexer=crear_lexer()
                )

                if nodo is not None:
                    raiz.agregar(nodo)

            except SyntaxCompilerError as e:
                errores.append(
                    f"Línea {linea}: ERROR SINTÁCTICO: {e}"
                )

            except SemanticError as e:
                errores.append(
                    f"Línea {linea}: ERROR SEMÁNTICO: {e}"
                )

            except Exception as e:
                errores.append(
                    f"Línea {linea}: ERROR: {e}"
                )

        codigo_intermedio = parser_ply.intermediate.obtener_codigo()
        tabla_simbolos = parser_ply.semantic.tabla.obtener_todos()

        return {
            "tokens": tokens_generados,
            "errores": errores,
            "arbol": raiz,
            "tabla_simbolos": tabla_simbolos,
            "codigo_intermedio": codigo_intermedio,
        }
