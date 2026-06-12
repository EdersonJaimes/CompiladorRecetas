import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from compiler import Compiler
from symbols import INGREDIENTES, UNIDADES_VALIDAS, ACCIONES_VALIDAS

# COLORES

BG = "#F4F8FC"
PANEL = "#EAF2FB"

AZUL = "#1565C0"
AZUL2 = "#42A5F5"

TEXTO = "#1E293B"

EDITOR_BG = "#FFFFFF"
GUTTER_BG = "#E8EEF6"
GUTTER_FG = "#90A4BE"

CONSOLA_BG = "#0F172A"
CONSOLA_TXT = "#E2E8F0"

VERDE = "#10B981"
ROJO = "#EF4444"
AMARILLO = "#F59E0B"


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

# Conjuntos derivados de symbols.py para la validación en vivo
INGREDIENTES_LIQUIDOS = {k for k, v in INGREDIENTES.items() if v == "LIQUIDO"}
INGREDIENTES_SOLIDOS = {k for k, v in INGREDIENTES.items() if v == "SOLIDO"}
INGREDIENTES_CONTABLES = {k for k, v in INGREDIENTES.items() if v == "CONTABLE"}

UNIDADES_TEXTO = {"ML": "ml", "GR": "gr", "UN": "un"}


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
            "1400x780"
        )

        self.window.configure(
            bg=BG
        )

        self.crear_interfaz()

        # Render inicial de números de línea + validación
        self.actualizar_numeros_linea()
        self.validar_en_vivo()

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
            text="Análisis Léxico • Sintáctico • Semántico ",
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

        # -----------------------------------------
        # EDITOR + NÚMEROS DE LÍNEA
        # -----------------------------------------

        editor_frame = tk.Frame(izq, bg=BG)

        editor_frame.pack(
            fill="both",
            expand=True
        )

        # Gutter de números de línea
        self.numeros = tk.Text(
            editor_frame,
            width=4,
            padx=4,
            bg=GUTTER_BG,
            fg=GUTTER_FG,
            font=("Consolas", 12),
            relief="flat",
            state="disabled",
            takefocus=0,
            wrap="none",
        )

        self.numeros.pack(
            side="left",
            fill="y"
        )

        self.editor = tk.Text(
            editor_frame,
            bg=EDITOR_BG,
            fg=TEXTO,
            font=("Consolas", 12),
            undo=True,
            wrap="none",
        )

        self.editor.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Scroll vertical sincronizado entre editor y gutter
        scroll = tk.Scrollbar(
            editor_frame,
            orient="vertical",
            command=self._scroll_ambos
        )

        scroll.pack(side="right", fill="y")

        self.editor.configure(yscrollcommand=self._on_editor_scroll)
        self.numeros.configure(yscrollcommand=scroll.set)
        self._scrollbar = scroll

        # Eventos para refrescar números de línea + validación en vivo
        self.editor.bind("<KeyRelease>", self._on_editor_change)
        self.editor.bind("<MouseWheel>", lambda e: self.window.after(1, self.actualizar_numeros_linea))
        self.editor.bind("<ButtonRelease>", lambda e: self.window.after(1, self.actualizar_numeros_linea))

        self.editor.insert(
            "1.0",
            RECETA_EJEMPLO
        )

        self.editor.tag_config(
            "warning",
            underline=True,
            foreground="#B91C1C",
            background="#FFF3CD"
        )

        # -----------------------------------------
        # ESTADO (validación en vivo)
        # -----------------------------------------

        self.estado = tk.Label(
            izq,
            text="✔ Sin errores",
            anchor="w",
            justify="left",
            bg=BG,
            fg="#2E7D32",
            font=("Segoe UI", 9),
            wraplength=700,
        )

        self.estado.pack(fill=tk.X, pady=(4, 5))

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
            width=550
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
        # TABLA DE SÍMBOLOS
        # =========================================

        tab_simbolos = tk.Frame(tabs)

        tabs.add(
            tab_simbolos,
            text="Tabla de Símbolos"
        )

        cols = ("nombre", "tipo", "valor", "lineas")

        self.tabla_simbolos = ttk.Treeview(
            tab_simbolos,
            columns=cols,
            show="headings",
        )

        self.tabla_simbolos.heading("nombre", text="Nombre")
        self.tabla_simbolos.heading("tipo", text="Tipo")
        self.tabla_simbolos.heading("valor", text="Valor")
        self.tabla_simbolos.heading("lineas", text="Líneas")

        self.tabla_simbolos.column("nombre", width=130, anchor="w")
        self.tabla_simbolos.column("tipo", width=170, anchor="w")
        self.tabla_simbolos.column("valor", width=90, anchor="center")
        self.tabla_simbolos.column("lineas", width=90, anchor="center")

        self.tabla_simbolos.pack(
            fill="both",
            expand=True
        )

        # =========================================
        # ÁRBOL SINTÁCTICO
        # =========================================

        tab_arbol = tk.Frame(tabs)

        tabs.add(
            tab_arbol,
            text="Árbol Sintáctico"
        )

        self.txt_arbol = tk.Text(
            tab_arbol,
            bg=CONSOLA_BG,
            fg=VERDE,
            font=("Consolas", 10)
        )

        self.txt_arbol.pack(
            fill="both",
            expand=True
        )

    # =================================================
    # SCROLL SINCRONIZADO ENTRE GUTTER Y EDITOR
    # =================================================

    def _scroll_ambos(self, *args):
        self.editor.yview(*args)
        self.numeros.yview(*args)

    def _on_editor_scroll(self, *args):
        self._scrollbar.set(*args)
        self.numeros.yview_moveto(args[0])

    def _on_editor_change(self, event=None):
        self.actualizar_numeros_linea()
        self.validar_en_vivo()

    # =================================================
    # NÚMEROS DE LÍNEA
    # =================================================

    def actualizar_numeros_linea(self):

        total_lineas = int(self.editor.index("end-1c").split(".")[0])

        contenido = "\n".join(str(n) for n in range(1, total_lineas + 1))

        self.numeros.config(state="normal")
        self.numeros.delete("1.0", tk.END)
        self.numeros.insert("1.0", contenido)
        self.numeros.config(state="disabled")

        # Mantener sincronizado el scroll vertical
        self.numeros.yview_moveto(self.editor.yview()[0])

    # =================================================
    # VALIDACIÓN EN VIVO
    # =================================================

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

        instrucciones_validas = {
            "AGREGAR", "REPETIR", "PRECALENTAR"
        }

        for numero, linea_original in enumerate(lineas):

            linea = linea_original.strip()

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

            partes = linea[:-1].split()

            if not partes:
                errores.append(
                    f"Línea {numero+1}: instrucción vacía"
                )
                self.marcar_linea(numero)
                continue

            palabra_clave = partes[0]

            # ==========================
            # AGREGAR
            # ==========================

            if palabra_clave == "AGREGAR":

                # Estructura: AGREGAR <ingrediente> <numero> <unidad>
                if len(partes) != 4:

                    errores.append(
                        f"Línea {numero+1}: AGREGAR debe tener la forma "
                        f"'AGREGAR <ingrediente> <cantidad> <unidad>;'"
                    )

                    self.marcar_linea(numero)
                    continue

                ingrediente = partes[1]
                cantidad_str = partes[2]
                unidad_str = partes[3]

                # Ingrediente debe ser identificador válido (mayúsculas)
                if not self._es_identificador(ingrediente):
                    errores.append(
                        f"Línea {numero+1}: '{ingrediente}' no es un "
                        f"identificador válido (use MAYÚSCULAS y guion bajo)"
                    )
                    self.marcar_linea(numero)

                # Cantidad debe ser numérica
                cantidad = None
                if not cantidad_str.isdigit():
                    errores.append(
                        f"Línea {numero+1}: '{cantidad_str}' no es una "
                        f"cantidad numérica válida"
                    )
                    self.marcar_linea(numero)
                else:
                    cantidad = int(cantidad_str)

                # Unidad debe ser ml, gr o un
                unidad = unidad_str.upper()
                if unidad not in UNIDADES_VALIDAS.values():
                    errores.append(
                        f"Línea {numero+1}: unidad inválida '{unidad_str}' "
                        f"(use ml, gr o un)"
                    )
                    self.marcar_linea(numero)

                # Ingrediente reconocido
                if self._es_identificador(ingrediente):

                    if ingrediente not in INGREDIENTES:
                        errores.append(
                            f"Línea {numero+1}: ingrediente desconocido "
                            f"'{ingrediente}'"
                        )
                        self.marcar_linea(numero)

                    else:
                        # Validar unidad correcta según tipo de ingrediente
                        tipo = INGREDIENTES[ingrediente]
                        unidad_correcta = UNIDADES_VALIDAS[tipo]

                        if unidad in UNIDADES_VALIDAS.values() and unidad != unidad_correcta:
                            errores.append(
                                f"Línea {numero+1}: {ingrediente} debe usar "
                                f"{UNIDADES_TEXTO[unidad_correcta]}"
                            )
                            self.marcar_linea(numero)

                # Validar rango de cantidad
                if cantidad is not None:

                    if cantidad <= 0:
                        errores.append(
                            f"Línea {numero+1}: la cantidad debe ser mayor a 0"
                        )
                        self.marcar_linea(numero)

                    elif cantidad > 10000:
                        errores.append(
                            f"Línea {numero+1}: cantidad excesiva (máximo 10000)"
                        )
                        self.marcar_linea(numero)

            # ==========================
            # PRECALENTAR
            # ==========================

            elif palabra_clave == "PRECALENTAR":

                # Estructura: PRECALENTAR <numero> °C
                if len(partes) != 3:
                    errores.append(
                        f"Línea {numero+1}: PRECALENTAR debe tener la forma "
                        f"'PRECALENTAR <temperatura> °C;'"
                    )
                    self.marcar_linea(numero)
                    continue

                temp_str = partes[1]
                grados_str = partes[2]

                if not temp_str.isdigit():
                    errores.append(
                        f"Línea {numero+1}: '{temp_str}' no es una "
                        f"temperatura numérica válida"
                    )
                    self.marcar_linea(numero)
                else:
                    temp = int(temp_str)

                    if temp < 50:
                        errores.append(
                            f"Línea {numero+1}: temperatura demasiado baja "
                            f"(mínimo 50°C)"
                        )
                        self.marcar_linea(numero)

                    elif temp > 250:
                        errores.append(
                            f"Línea {numero+1}: temperatura demasiado alta "
                            f"(máximo 250°C)"
                        )
                        self.marcar_linea(numero)

                if grados_str != "°C":
                    errores.append(
                        f"Línea {numero+1}: se esperaba '°C' después de la "
                        f"temperatura"
                    )
                    self.marcar_linea(numero)

            # ==========================
            # REPETIR
            # ==========================

            elif palabra_clave == "REPETIR":

                # Estructura: REPETIR <numero> VECES <accion>
                if len(partes) != 4:
                    errores.append(
                        f"Línea {numero+1}: REPETIR debe tener la forma "
                        f"'REPETIR <n> VECES <accion>;'"
                    )
                    self.marcar_linea(numero)
                    continue

                veces_str = partes[1]
                veces_kw = partes[2]
                accion = partes[3]

                if not veces_str.isdigit():
                    errores.append(
                        f"Línea {numero+1}: '{veces_str}' no es un número "
                        f"válido de repeticiones"
                    )
                    self.marcar_linea(numero)
                else:
                    veces = int(veces_str)

                    if veces <= 0:
                        errores.append(
                            f"Línea {numero+1}: el número de repeticiones "
                            f"debe ser mayor a 0"
                        )
                        self.marcar_linea(numero)

                    elif veces > 100:
                        errores.append(
                            f"Línea {numero+1}: número de repeticiones "
                            f"excesivo (máximo 100)"
                        )
                        self.marcar_linea(numero)

                if veces_kw != "VECES":
                    errores.append(
                        f"Línea {numero+1}: se esperaba la palabra clave "
                        f"'VECES'"
                    )
                    self.marcar_linea(numero)

                if accion not in ACCIONES_VALIDAS:
                    errores.append(
                        f"Línea {numero+1}: acción inválida '{accion}'"
                    )
                    self.marcar_linea(numero)

            # ==========================
            # ASIGNACIÓN: VAR = VALOR
            # ==========================

            elif "=" in linea:

                if len(partes) != 3 or partes[1] != "=":
                    errores.append(
                        f"Línea {numero+1}: asignación inválida, use "
                        f"'VARIABLE = VALOR;'"
                    )
                    self.marcar_linea(numero)
                    continue

                variable, _, valor = partes

                if not self._es_identificador(variable):
                    errores.append(
                        f"Línea {numero+1}: '{variable}' no es un "
                        f"identificador válido"
                    )
                    self.marcar_linea(numero)

                if not self._es_identificador(valor):
                    errores.append(
                        f"Línea {numero+1}: '{valor}' no es un "
                        f"identificador válido"
                    )
                    self.marcar_linea(numero)

            # ==========================
            # PALABRA CLAVE DESCONOCIDA
            # ==========================

            else:

                errores.append(
                    f"Línea {numero+1}: instrucción desconocida "
                    f"'{palabra_clave}'. Use AGREGAR, REPETIR, "
                    f"PRECALENTAR o una asignación."
                )

                self.marcar_linea(numero)

        # ==========================
        # MOSTRAR RESULTADO
        # ==========================

        if errores:

            if len(errores) == 1:
                texto_estado = "⚠ " + errores[0]
            else:
                texto_estado = (
                    f"⚠ {len(errores)} problemas encontrados — "
                    f"{errores[0]}"
                )

            self.estado.config(
                text=texto_estado,
                fg="#D32F2F"
            )

        else:

            self.estado.config(
                text="✔ Sin errores",
                fg="#2E7D32"
            )

    def _es_identificador(self, texto):
        """Replica el patrón [A-Z_][A-Z_0-9]* del lexer."""

        if not texto:
            return False

        if not (texto[0].isalpha() and texto[0].isupper() or texto[0] == "_"):
            return False

        for c in texto[1:]:
            if not ((c.isalpha() and c.isupper()) or c.isdigit() or c == "_"):
                return False

        return True

    def marcar_linea(self, numero_linea):

        inicio = f"{numero_linea+1}.0"

        fin = f"{numero_linea+1}.end"

        self.editor.tag_add(
            "warning",
            inicio,
            fin
        )

    # =================================================
    # COMPILACIÓN
    # =================================================

    def compilar(self):

        codigo = self.editor.get(
            "1.0",
            tk.END
        )

        self.txt_tokens.delete("1.0", tk.END)
        self.txt_errores.delete("1.0", tk.END)
        self.txt_arbol.delete("1.0", tk.END)

        for fila in self.tabla_simbolos.get_children():
            self.tabla_simbolos.delete(fila)

        try:

            resultado = self.compiler.compilar(codigo)

            # --- TOKENS ---
            for token in resultado["tokens"]:
                self.txt_tokens.insert(tk.END, f"{token}\n")

            # --- ERRORES ---
            errores = resultado["errores"]

            if errores:
                for err in errores:
                    self.txt_errores.insert(tk.END, f"{err}\n")
            else:
                self.txt_errores.insert(
                    tk.END, "✔ No se encontraron errores.\n"
                )

            # --- ÁRBOL SINTÁCTICO ---
            arbol = resultado["arbol"]
            if arbol.hijos:
                self.txt_arbol.insert(tk.END, str(arbol))
            else:
                self.txt_arbol.insert(
                    tk.END, "(no se generó ningún nodo válido)"
                )

            # --- TABLA DE SÍMBOLOS ---
            for nombre, info in resultado["tabla_simbolos"].items():

                lineas_str = ", ".join(str(l) for l in info["usos"])

                self.tabla_simbolos.insert(
                    "", tk.END,
                    values=(nombre, info["tipo"], info["valor"], lineas_str)
                )

            # --- MENSAJE FINAL ---
            if errores:
                messagebox.showwarning(
                    "Compilación con errores",
                    f"Se encontraron {len(errores)} error(es). "
                    f"Revisa la pestaña 'Errores'."
                )
            else:
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

        self.editor.delete("1.0", tk.END)
        self.txt_tokens.delete("1.0", tk.END)
        self.txt_errores.delete("1.0", tk.END)
        self.txt_arbol.delete("1.0", tk.END)

        for fila in self.tabla_simbolos.get_children():
            self.tabla_simbolos.delete(fila)

        self.actualizar_numeros_linea()
        self.validar_en_vivo()

    # =================================================

    def cargar_ejemplo(self):

        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", RECETA_EJEMPLO)

        self.actualizar_numeros_linea()
        self.validar_en_vivo()

    # =================================================

    def ejecutar(self):

        self.window.mainloop()
