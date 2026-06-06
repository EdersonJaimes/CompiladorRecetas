import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from compiler import Compiler

# COLORES

BG = "#F4F8FC"
PANEL = "#EAF2FB"

AZUL = "#1565C0"
AZUL2 = "#42A5F5"

TEXTO = "#1E293B"

EDITOR_BG = "#FFFFFF"

CONSOLA_BG = "#0F172A"
CONSOLA_TXT = "#E2E8F0"

VERDE = "#10B981"
ROJO = "#EF4444"


# =====================================================
# RECETA DE EJEMPLO
# =====================================================

RECETA_EJEMPLO = """PRECALENTAR 180 °C;

AGREGAR HARINA 250 gr;
AGREGAR AZUCAR 200 gr;
AGREGAR CACAO 50 gr;
AGREGAR POLVO_HORNEAR 10 gr;

AGREGAR MANTEQUILLA 120 gr;
AGREGAR HUEVOS 3 un;

AGREGAR LECHE 100 ml;
AGREGAR VAINILLA 5 ml;

REPETIR 3 VECES CERNIR;
REPETIR 5 VECES MEZCLAR;
REPETIR 8 VECES BATIR;

REPETIR 1 VECES ENGRASAR;
REPETIR 1 VECES HORNEAR;
REPETIR 1 VECES ENFRIAR;

REPETIR 2 VECES DECORAR;
"""


# =====================================================
# GUI
# =====================================================

class CompilerGUI:

    def __init__(self):

        self.compiler = Compiler()

        self.window = tk.Tk()

        self.window.title(
            "Compilador DSL Recetas Dulces"
        )

        self.window.geometry(
            "1350x750"
        )

        self.window.configure(
            bg=BG
        )

        self.crear_interfaz()

    # =================================================

    def crear_interfaz(self):

        # -----------------------------------------
        # TÍTULO
        # -----------------------------------------

        titulo = tk.Frame(
            self.window,
            bg=AZUL,
            height=70
        )

        titulo.pack(
            fill="x"
        )

        tk.Label(
            titulo,
            text="🎂 COMPILADOR DSL - RECETAS DULCES",
            bg=AZUL,
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=(10, 0)
        )

        tk.Label(
            titulo,
            text="Análisis Léxico • Sintáctico • Semántico • Código Intermedio",
            bg=AZUL,
            fg="white",
            font=("Segoe UI", 10)
        ).pack()

        # -----------------------------------------
        # CONTENEDOR
        # -----------------------------------------

        contenedor = tk.Frame(
            self.window,
            bg=BG
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # -----------------------------------------
        # PANEL IZQUIERDO
        # -----------------------------------------

        izq = tk.Frame(
            contenedor,
            bg=BG
        )

        izq.pack(
            side="left",
            fill="both",
            expand=True
        )

        tk.Label(
            izq,
            text="Editor de Recetas",
            bg=BG,
            fg=TEXTO,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        self.editor = tk.Text(
            izq,
            bg=EDITOR_BG,
            fg=TEXTO,
            font=("Consolas", 12),
            undo=True
        )

        self.editor.pack(
            fill="both",
            expand=True
        )

        self.editor.insert(
            "1.0",
            RECETA_EJEMPLO
        )

        # -----------------------------------------
        # BOTONES
        # -----------------------------------------

        barra = tk.Frame(
            izq,
            bg=BG
        )

        barra.pack(
            fill="x",
            pady=10
        )

        tk.Button(
            barra,
            text="▶ Compilar",
            bg=AZUL,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.compilar
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            barra,
            text="🗑 Limpiar",
            bg=AZUL2,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.limpiar
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            barra,
            text="📋 Cargar Ejemplo",
            bg="#64748B",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.cargar_ejemplo
        ).pack(
            side="left",
            padx=5
        )

        # -----------------------------------------
        # PANEL DERECHO
        # -----------------------------------------

        der = tk.Frame(
            contenedor,
            bg=PANEL,
            width=500
        )

        der.pack(
            side="right",
            fill="both"
        )

        der.pack_propagate(False)

        # -----------------------------------------
        # NOTEBOOK
        # -----------------------------------------

        tabs = ttk.Notebook(
            der
        )

        tabs.pack(
            fill="both",
            expand=True
        )

        # =========================================
        # TOKENS
        # =========================================

        tab_tokens = tk.Frame(tabs)

        tabs.add(
            tab_tokens,
            text="Tokens"
        )

        self.txt_tokens = tk.Text(
            tab_tokens,
            bg=CONSOLA_BG,
            fg=CONSOLA_TXT,
            font=("Consolas", 10)
        )

        self.txt_tokens.pack(
            fill="both",
            expand=True
        )

        # =========================================
        # ERRORES
        # =========================================

        tab_errores = tk.Frame(tabs)

        tabs.add(
            tab_errores,
            text="Errores"
        )

        self.txt_errores = tk.Text(
            tab_errores,
            bg=CONSOLA_BG,
            fg=ROJO,
            font=("Consolas", 10)
        )

        self.txt_errores.pack(
            fill="both",
            expand=True
        )

        # =========================================
        # CÓDIGO INTERMEDIO
        # =========================================

        tab_ci = tk.Frame(tabs)

        tabs.add(
            tab_ci,
            text="Código Intermedio"
        )

        self.txt_ci = tk.Text(
            tab_ci,
            bg=CONSOLA_BG,
            fg=VERDE,
            font=("Consolas", 10)
        )

        self.txt_ci.pack(
            fill="both",
            expand=True
        )

    # =================================================

    def compilar(self):

        codigo = self.editor.get(
            "1.0",
            tk.END
        )

        self.txt_tokens.delete(
            "1.0",
            tk.END
        )

        self.txt_errores.delete(
            "1.0",
            tk.END
        )

        self.txt_ci.delete(
            "1.0",
            tk.END
        )

        try:

            tokens, codigo_intermedio = (
                self.compiler.compilar(
                    codigo
                )
            )

            for token in tokens:

                self.txt_tokens.insert(
                    tk.END,
                    f"{token}\n"
                )

            self.txt_ci.insert(
                tk.END,
                codigo_intermedio
            )

            messagebox.showinfo(
                "Compilación",
                "La receta fue compilada correctamente."
            )

        except Exception as e:

            self.txt_errores.insert(
                tk.END,
                str(e)
            )

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =================================================

    def limpiar(self):

        self.editor.delete(
            "1.0",
            tk.END
        )

        self.txt_tokens.delete(
            "1.0",
            tk.END
        )

        self.txt_errores.delete(
            "1.0",
            tk.END
        )

        self.txt_ci.delete(
            "1.0",
            tk.END
        )

    # =================================================

    def cargar_ejemplo(self):

        self.editor.delete(
            "1.0",
            tk.END
        )

        self.editor.insert(
            "1.0",
            RECETA_EJEMPLO
        )

    # =================================================

    def ejecutar(self):

        self.window.mainloop()