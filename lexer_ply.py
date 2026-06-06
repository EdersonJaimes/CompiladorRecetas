import ply.lex as lex

# PALABRAS RESERVADAS
reserved = {
    "AGREGAR": "AGREGAR",
    "REPETIR": "REPETIR",
    "VECES": "VECES",
    "MEZCLAR": "MEZCLAR",
    "BATIR": "BATIR",
    "HORNEAR": "HORNEAR",
    "DECORAR": "DECORAR",
    "ENGRASAR": "ENGRASAR",
    "PRECALENTAR": "PRECALENTAR",
    "VERTER": "VERTER",
    "ENFRIAR": "ENFRIAR",
    "CERNIR": "CERNIR"
}

# TOKENS
tokens = [
    "NUMERO",
    "ML",
    "GR",
    "UN",
    "C",
    "IGUAL",
    "PUNTO_COMA",
    "IDENTIFICADOR"
] + list(reserved.values())

# TOKENS SIMPLES
t_IGUAL = r'='
t_PUNTO_COMA = r';'
t_ML = r'ml'
t_GR = r'gr'
t_UN = r'un'
t_C = r'°C'

# NUMEROS
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# IDENTIFICADORES
def t_IDENTIFICADOR(t):
    r'[A-Z_][A-Z_0-9]*'
    t.type = reserved.get(
        t.value,
        "IDENTIFICADOR"
    )

    return t

# ESPACIOS
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# ERRORES
def t_error(t):

    raise Exception(
        f"ERROR LÉXICO: símbolo inválido '{t.value[0]}'"
    )

lexer = lex.lex()