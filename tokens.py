TOKENS = [
    # Instrucciones
    ('AGREGAR', r'AGREGAR'),
    ('REPETIR', r'REPETIR'),
    ('VECES', r'VECES'),

    # Acciones
    ('MEZCLAR',     r'MEZCLAR'),
    ('BATIR',       r'BATIR'),
    ('HORNEAR',     r'HORNEAR'),
    ('DECORAR',     r'DECORAR'),
    ('ENGRASAR',    r'ENGRASAR'),
    ('PRECALENTAR', r'PRECALENTAR'),
    ('VERTER',      r'VERTER'),
    ('ENFRIAR',     r'ENFRIAR'),
    ('CERNIR',      r'CERNIR'),

    # Unidades
    ('ML', r'ml'),
    ('GR', r'gr'),
    ('UN', r'un'),       # unidades (huevos, etc.)
    ('C',  r'°C'),       # grados Celsius (para PRECALENTAR)

    # Literales
    ('NUMERO', r'\d+'),

    # Símbolos
    ('IGUAL',      r'='),
    ('PUNTO_COMA', r';'),

    # Identificadores y espacios
    ('IDENTIFICADOR', r'[A-Z_][A-Z_0-9]*'),
    ('ESPACIO', r'[ \t\n]+'),
    ('ERROR',   r'.'),
]
