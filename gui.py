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
            "Compilador de Recetas"
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

        self.editor.bind(
            "<KeyRelease>",
            self.validar_en_vivo
        )

        self.editor.pack(
            fill="both",
            expand=True
        )

        self.estado = tk.Label(
            izq,
            text="✔ Sin errores",
            anchor="w",
            bg=BG,
            fg="#2E7D32",
            font=("Segoe UI", 9)
        )

        self.editor.insert(
            "1.0",
            RECETA_EJEMPLO
        )

        self.editor.tag_config(
            "warning",
            underline=True,
            foreground="red",
            background="#FFF3CD"
        )

        self.editor.tag_config(
            "error",
            foreground="white",
            background="#E74C3C"
        )

        self.estado = tk.Label(
            izq,
            text="✔ Sin errores",
            anchor="w",
            bg=BG,
            fg="#2E7D32",
            font=("Segoe UI", 9)
        )

        self.estado.pack(fill=tk.X, pady=(2,5))

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

    def validar_en_vivo(self, event=None):

        self.editor.tag_remove(
            "warning",
            "1.0",
            tk.END
        )

        errores = []

        texto = self.editor.get(
            "1.0",
            tk.END
        )

        lineas = texto.splitlines()

        ingredientes_validos = {
            'AGUA','LECHE','ACEITE','VAINILLA',
            'CREMA','RON','CAFE',
            'HARINA','AZUCAR','SAL',
            'CHOCOLATE','MANTEQUILLA',
            'FRESA','CACAO',
            'POLVO_HORNEAR',
            'BICARBONATO',
            'MAICENA',
            'QUESO_CREMA',
            'AZUCAR_GLASS',
            'CANELA',
            'NUEZ',
            'COCO',
            'HUEVO',
            'HUEVOS',
            'YEMA',
            'YEMAS',
            'CLARA',
            'CLARAS'
        }

        acciones_validas = {
            'MEZCLAR',
            'BATIR',
            'HORNEAR',
            'DECORAR',
            'ENGRASAR',
            'VERTER',
            'ENFRIAR',
            'CERNIR'
        }

        for numero, linea in enumerate(lineas):

            linea = linea.strip()

            if not linea:
                continue

            # ==========================
            # FALTA ;
            # ==========================

            if not linea.endswith(";"):

                errores.append(
                    f"Línea {numero+1}: falta ';'"
                )

                self.marcar_linea(numero)

                continue

            partes = linea.replace(
                ";",
                ""
            ).split()

            # ==========================
            # AGREGAR
            # ==========================

            if linea.startswith("AGREGAR"):

                if len(partes) >= 4:

                    ingrediente = partes[1]

                    try:
                        cantidad = int(partes[2])
                    except:
                        cantidad = None

                    unidad = partes[3].upper()

                    if ingrediente not in ingredientes_validos:

                        errores.append(
                            f"Línea {numero+1}: ingrediente desconocido '{ingrediente}'"
                        )

                        self.marcar_linea(numero)

                    if ingrediente in {
                        'LECHE','AGUA','ACEITE',
                        'VAINILLA','CREMA',
                        'RON','CAFE'
                    }:

                        if unidad != "ML":

                            errores.append(
                                f"Línea {numero+1}: {ingrediente} debe usar ml"
                            )

                            self.marcar_linea(numero)

                    if ingrediente in {
                        'HARINA','AZUCAR',
                        'SAL','CHOCOLATE',
                        'MANTEQUILLA',
                        'FRESA','CACAO',
                        'POLVO_HORNEAR',
                        'BICARBONATO',
                        'MAICENA',
                        'QUESO_CREMA',
                        'AZUCAR_GLASS',
                        'CANELA',
                        'NUEZ',
                        'COCO'
                    }:

                        if unidad != "GR":

                            errores.append(
                                f"Línea {numero+1}: {ingrediente} debe usar gr"
                            )

                            self.marcar_linea(numero)

                    if ingrediente in {
                        'HUEVO',
                        'HUEVOS',
                        'YEMA',
                        'YEMAS',
                        'CLARA',
                        'CLARAS'
                    }:

                        if unidad != "UN":

                            errores.append(
                                f"Línea {numero+1}: {ingrediente} debe usar un"
                            )

                            self.marcar_linea(numero)

            # ==========================
            # PRECALENTAR
            # ==========================

            elif linea.startswith("PRECALENTAR"):

                if len(partes) >= 3:

                    try:

                        temp = int(
                            partes[1]
                        )

                        if temp < 50:

                            errores.append(
                                f"Línea {numero+1}: temperatura demasiado baja"
                            )

                            self.marcar_linea(numero)

                        elif temp > 250:

                            errores.append(
                                f"Línea {numero+1}: temperatura demasiado alta"
                            )

                            self.marcar_linea(numero)

                    except:
                        pass

            # ==========================
            # REPETIR
            # ==========================

            elif linea.startswith("REPETIR"):

                if len(partes) >= 4:

                    accion = partes[3]

                    if accion not in acciones_validas:

                        errores.append(
                            f"Línea {numero+1}: acción inválida '{accion}'"
                        )

                        self.marcar_linea(numero)

        # ==========================
        # MOSTRAR RESULTADO
        # ==========================

        if errores:

            self.estado.config(
                text=errores[0],
                fg="#D32F2F"
            )

        else:

            self.estado.config(
                text="✔ Sin errores",
                fg="#2E7D32"
            )

    def marcar_linea(self, numero_linea):

        inicio = f"{numero_linea+1}.0"

        fin = f"{numero_linea+1}.end"

        self.editor.tag_add(
            "warning",
            inicio,
            fin
        )

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