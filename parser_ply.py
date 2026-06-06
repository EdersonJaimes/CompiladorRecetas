import ply.yacc as yacc

from lexer_ply import tokens
from semantic import SemanticAnalyzer
from intermediate_code import IntermediateCodeGenerator
from ast_node import ASTNode


semantic = SemanticAnalyzer()
intermediate = None

# PROGRAMA
def p_programa(p):
    '''
    programa : instrucciones
    '''
    p[0] = "Programa válido"


# LISTA DE INSTRUCCIONES
def p_instrucciones_multiple(p):
    '''
    instrucciones : instrucciones instruccion
    '''
    pass


def p_instrucciones_simple(p):
    '''
    instrucciones : instruccion
    '''
    pass


# AGREGAR
# AGREGAR HARINA 250 gr;
def p_instruccion_agregar(p):
    '''
    instruccion : AGREGAR IDENTIFICADOR NUMERO unidad PUNTO_COMA
    '''
    ingrediente = p[2]
    cantidad = p[3]
    unidad = p[4]

    semantic.validar_cantidad(cantidad)

    semantic.validar_agregar(
        ingrediente,
        unidad
    )

    intermediate.agregar(
        ingrediente,
        cantidad,
        unidad.lower()
    )


# PRECALENTAR
# PRECALENTAR 180 °C;

def p_instruccion_precalentar(p):
    '''
    instruccion : PRECALENTAR NUMERO C PUNTO_COMA
    '''

    temperatura = p[2]

    semantic.validar_temperatura(
        temperatura
    )

    intermediate.precalentar(
        temperatura
    )

# REPETIR
# REPETIR 5 VECES BATIR;
def p_instruccion_repetir(p):
    '''
    instruccion : REPETIR NUMERO VECES accion PUNTO_COMA
    '''

    veces = p[2]
    accion = p[4]

    intermediate.repetir(
        veces,
        accion
    )


# ASIGNACION
# RELLENO = CHOCOLATE;
def p_instruccion_asignacion(p):
    '''
    instruccion : IDENTIFICADOR IGUAL IDENTIFICADOR PUNTO_COMA
    '''

    variable = p[1]
    valor = p[3]

    intermediate.asignacion(
        variable,
        valor
    )


# UNIDADES
def p_unidad_ml(p):
    '''
    unidad : ML
    '''
    p[0] = "ML"


def p_unidad_gr(p):
    '''
    unidad : GR
    '''
    p[0] = "GR"


def p_unidad_un(p):
    '''
    unidad : UN
    '''
    p[0] = "UN"

# ACCIONES
def p_accion_mezclar(p):
    '''
    accion : MEZCLAR
    '''
    p[0] = "MEZCLAR"


def p_accion_batir(p):
    '''
    accion : BATIR
    '''
    p[0] = "BATIR"


def p_accion_hornear(p):
    '''
    accion : HORNEAR
    '''
    p[0] = "HORNEAR"


def p_accion_decorar(p):
    '''
    accion : DECORAR
    '''
    p[0] = "DECORAR"


def p_accion_engrasar(p):
    '''
    accion : ENGRASAR
    '''
    p[0] = "ENGRASAR"


def p_accion_verter(p):
    '''
    accion : VERTER
    '''
    p[0] = "VERTER"


def p_accion_enfriar(p):
    '''
    accion : ENFRIAR
    '''
    p[0] = "ENFRIAR"


def p_accion_cernir(p):
    '''
    accion : CERNIR
    '''
    p[0] = "CERNIR"

def reiniciar_generador():

    global intermediate

    intermediate = IntermediateCodeGenerator()

# ERROR SINTACTICO
def p_error(p):

    if p:

        raise Exception(
            f"ERROR SINTÁCTICO: token inesperado "
            f"'{p.value}'"
        )

    raise Exception(
        "ERROR SINTÁCTICO: fin inesperado del archivo"
    )

parser = yacc.yacc()