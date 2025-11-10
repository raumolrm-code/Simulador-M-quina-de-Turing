# InterfazMT.py
# Este archivo dibuja la ventana, la cinta y el cabezal con Tkinter.
# La clase usa MotorMT para avanzar y muestra el resultado en pantalla.

import tkinter as tk
from tkinter import ttk

from TemaColores import (
    COLORFONDO, COLORPANEL, COLORCELDA, COLOROK, COLORAVISO, COLORERROR,
    COLORTEXTO, COLORTENUE, COLORCABEZA, COLORPROC
)
from EspecificacionesLenguajes import EspecificacionesLenguajes, BLANCO, EPSILON
from MotorMT import MotorMT

class InterfazMT(tk.Tk):
    def __init__(self):
        super().__init__()

        # Se configura la ventana principal.
        self.title("Simulador MT — Lenguajes Regulares")
        self.geometry("1120x620")
        self.minsize(980, 560)
        self.configure(bg=COLORFONDO)

        # Se cargan los lenguajes y se crea el motor.
        self.especificaciones = EspecificacionesLenguajes.obtenerLista()
        self.motor = MotorMT(self.especificaciones[0])

        # Se definen banderas de animación.
        self.enEjecucion = False
        self.enRebobinado = False
        self.retrasoMs = 320

        # Se arma la interfaz.
        self.configurarEstilos()
        self.crearInterfaz()
        self.activarEventos()

        # Se selecciona un lenguaje por defecto.
        self.comboLenguaje.current(0)
        self.mostrarLenguaje(0)

    # Se configuran estilos ttk para que la interfaz se vea ordenada.
    def configurarEstilos(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use('clam')
        except:
            pass
        estilo.configure("TFrame", background=COLORFONDO)
        estilo.configure("TLabel", background=COLORFONDO, foreground=COLORTEXTO)
        estilo.configure("TLabelframe", background=COLORFONDO, foreground=COLORTEXTO)
        estilo.configure("TLabelframe.Label", background=COLORFONDO, foreground=COLORTEXTO)
        estilo.configure("TButton", padding=6)
        estilo.map("TButton",
                   foreground=[("disabled", "#9ca3af")],
                   background=[("active", "#1f2937")])

    # Se crea toda la interfaz: panel de controles y panel de cinta.
    def crearInterfaz(self):
        # Encabezado
        cabecera = tk.Frame(self, bg=COLORPANEL)
        cabecera.pack(side=tk.TOP, fill=tk.X)
        tk.Label(cabecera, text="Simulador de Máquina de Turing",
                 font=("Segoe UI", 16, "bold"), fg=COLORTEXTO, bg=COLORPANEL).pack(side=tk.LEFT, padx=14, pady=10)
        tk.Label(cabecera, text="Validación de lenguajes regulares",
                 font=("Segoe UI", 10), fg=COLORTENUE, bg=COLORPANEL).pack(side=tk.LEFT, padx=8)

        # Cuerpo
        cuerpo = tk.Frame(self, bg=COLORFONDO)
        cuerpo.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel izquierdo (controles)
        panelIzq = tk.Frame(cuerpo, bg=COLORPANEL, width=320)
        panelIzq.pack(side=tk.LEFT, fill=tk.Y)
        panelIzq.pack_propagate(False)

        tk.Label(panelIzq, text="Lenguaje", font=("Segoe UI", 10, "bold"),
                 fg=COLORTEXTO, bg=COLORPANEL).pack(anchor="w", padx=12, pady=(14, 2))
        self.comboLenguaje = ttk.Combobox(panelIzq, state="readonly",
                                          values=[sp["nombre"] for sp in self.especificaciones])
        self.comboLenguaje.pack(fill=tk.X, padx=12)

        tk.Label(panelIzq, text="Cadena de entrada", font=("Segoe UI", 10, "bold"),
                 fg=COLORTEXTO, bg=COLORPANEL).pack(anchor="w", padx=12, pady=(14, 2))
        self.cajaEntrada = ttk.Entry(panelIzq, font=("Consolas", 12))
        self.cajaEntrada.pack(fill=tk.X, padx=12)

        cajaBotones = tk.Frame(panelIzq, bg=COLORPANEL)
        cajaBotones.pack(fill=tk.X, padx=8, pady=12)

        self.btnIniciar = ttk.Button(cajaBotones, text="Iniciar", command=self.iniciar)
        self.btnIniciar.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

        self.btnPaso = ttk.Button(cajaBotones, text="Paso", command=self.paso, state=tk.DISABLED)
        self.btnPaso.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

        self.btnCorrer = ttk.Button(cajaBotones, text="Correr", command=self.alternarCorrer, state=tk.DISABLED)
        self.btnCorrer.grid(row=1, column=0, padx=6, pady=6, sticky="ew")

        self.btnReiniciar = ttk.Button(cajaBotones, text="Reiniciar", command=self.reiniciarUi, state=tk.DISABLED)
        self.btnReiniciar.grid(row=1, column=1, padx=6, pady=6, sticky="ew")

        for c in range(2):
            cajaBotones.grid_columnconfigure(c, weight=1)

        panelEstado = tk.Frame(panelIzq, bg=COLORPANEL)
        panelEstado.pack(fill=tk.X, padx=10, pady=(6, 10))
        tk.Label(panelEstado, text="Estado actual:",
                 font=("Segoe UI", 10), fg=COLORTENUE, bg=COLORPANEL).grid(row=0, column=0, sticky="w")
        self.lblEstado = tk.Label(panelEstado, text="—", font=("Consolas", 18, "bold"),
                                  fg=COLORTEXTO, bg=COLORPANEL)
        self.lblEstado.grid(row=1, column=0, sticky="w", pady=(2, 6))
        self.lblResultado = tk.Label(panelEstado, text="", font=("Segoe UI", 12, "bold"),
                                     fg=COLORTEXTO, bg=COLORPANEL)
        self.lblResultado.grid(row=2, column=0, sticky="w")
        tk.Label(panelEstado, text="Leyenda:",
                 font=("Segoe UI", 10, "bold"), fg=COLORTENUE, bg=COLORPANEL).grid(row=3, column=0, sticky="w", pady=(12, 2))
        tk.Label(panelEstado, text=f"{EPSILON} = procesado   |   {BLANCO} = fin de cadena",
                 font=("Segoe UI", 9), fg=COLORTENUE, bg=COLORPANEL).grid(row=4, column=0, sticky="w")

        # Panel derecho (cinta)
        panelDer = tk.Frame(cuerpo, bg=COLORFONDO)
        panelDer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0))

        tk.Label(panelDer, text="Cinta",
                 font=("Segoe UI", 12, "bold"), fg=COLORTEXTO, bg=COLORFONDO).pack(anchor="w", pady=(0, 6))

        areaCinta = tk.Frame(panelDer, bg=COLORFONDO)
        areaCinta.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(areaCinta, height=160, bg=COLORFONDO, highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.barraX = ttk.Scrollbar(areaCinta, orient="horizontal", command=self.canvas.xview)
        self.barraX.pack(side=tk.TOP, fill=tk.X)
        self.canvas.configure(xscrollcommand=self.barraX.set)
        self.canvas.configure(xscrollincrement=1)

        self.marcoCinta = tk.Frame(self.canvas, bg=COLORFONDO)
        self.canvasWin = self.canvas.create_window((0, 0), window=self.marcoCinta, anchor="nw")

        self.lblCeldas = []
        self.lblFlechas = []

        # Mensaje bajo la cinta (lo que “se esperaba” en rechazo)
        self.lblEsperado = tk.Label(panelDer, text="", font=("Segoe UI", 11),
                                    fg=COLORERROR, bg=COLORFONDO, anchor="w", justify="left")
        self.lblEsperado.pack(fill=tk.X, pady=(8, 0))

        self.marcoCinta.bind("<Configure>", lambda e: self.actualizarScrollRegion())
        self.canvas.bind("<Configure>", lambda e: self.actualizarScrollRegion())
        self.after(50, self.actualizarScrollRegion)

    # Se activan eventos de la interfaz (por ejemplo, cambio de lenguaje).
    def activarEventos(self):
        self.comboLenguaje.bind("<<ComboboxSelected>>", self.cuandoCambiaLenguaje)

    # Se mantiene el área de scroll actualizada al tamaño del contenido.
    def actualizarScrollRegion(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Se cambia el lenguaje cuando el usuario elige otro.
    def cuandoCambiaLenguaje(self, _evt):
        self.mostrarLenguaje(self.comboLenguaje.current())

    # Se muestra el lenguaje indicado y se reinicia la interfaz.
    def mostrarLenguaje(self, idx):
        self.motor.cargarEspecificacion(self.especificaciones[idx])
        self.reiniciarUi(fresco=True)

    # Se restablecen los controles y la cinta a su estado inicial.
    def reiniciarUi(self, fresco=False):
        self.enEjecucion = False
        self.enRebobinado = False
        self.lblEstado.configure(text=f"q{self.motor.especActual['start_state']}", fg=COLORTEXTO)
        self.lblResultado.configure(text="", fg=COLORTEXTO)
        self.lblEsperado.configure(text="")
        self.btnPaso.configure(state=tk.DISABLED)
        self.btnCorrer.configure(state=tk.DISABLED)
        self.btnReiniciar.configure(state=tk.DISABLED)
        self.dibujarCinta([])

    # Se prepara la cinta con la cadena que el usuario ingresa.
    def construirCintaInicial(self, texto):
        self.motor.reiniciarConCadena(texto)

    # Se dibuja la cinta en pantalla con una celda extra para el blanco.
    def dibujarCinta(self, lista):
        for w in self.lblCeldas: w.destroy()
        for w in self.lblFlechas: w.destroy()
        self.lblCeldas.clear()
        self.lblFlechas.clear()

        total = len(lista) + 1  # +1 para mostrar el blanco
        for i in range(total):
            cont = tk.Frame(self.marcoCinta, bg=COLORFONDO)
            cont.grid(row=0, column=i, padx=3, pady=(8, 2))

            tarjeta = tk.Frame(cont, bg=COLORCELDA, bd=0,
                               highlightthickness=2, highlightbackground=COLORFONDO)
            tarjeta.pack(padx=2, pady=2)

            lbl = tk.Label(tarjeta, width=2, height=1, font=("Consolas", 18, "bold"),
                           bg=COLORCELDA, fg=COLORTEXTO)
            if i < len(lista):
                lbl.configure(text=lista[i])
            else:
                lbl.configure(text=BLANCO, fg=COLORTENUE)
            lbl.pack(padx=10, pady=10)
            self.lblCeldas.append(lbl)

            contFlecha = tk.Frame(self.marcoCinta, bg=COLORFONDO)
            contFlecha.grid(row=1, column=i, padx=3, pady=(0, 8))
            flecha = tk.Label(contFlecha, text=" ", font=("Segoe UI", 14, "bold"),
                              fg=COLORCABEZA, bg=COLORFONDO)
            flecha.pack()
            self.lblFlechas.append(flecha)

        self.resaltarCabezal()
        self.after(10, self.actualizarScrollRegion)
        self.after(20, self.asegurarCabezalVisible)

    # Se resalta la celda donde está el cabezal y se coloca la flecha ▼.
    def resaltarCabezal(self):
        for i, lbl in enumerate(self.lblCeldas):
            tarjeta = lbl.master
            if i == self.motor.cabezal:
                tarjeta.configure(highlightbackground=COLORCABEZA, highlightcolor=COLORCABEZA)
                if i < len(self.lblFlechas):
                    self.lblFlechas[i].configure(text="▼", fg=COLORCABEZA)
            else:
                tarjeta.configure(highlightbackground=COLORFONDO, highlightcolor=COLORFONDO)
                if i < len(self.lblFlechas):
                    self.lblFlechas[i].configure(text=" ", fg=COLORFONDO)
        self.asegurarCabezalVisible()

    # Se asegura que el cabezal quede visible moviendo el scroll si hace falta.
    def asegurarCabezalVisible(self, margen=40):
        try:
            anchoTotal = max(1, self.marcoCinta.winfo_reqwidth())
            anchoVista = max(1, self.canvas.winfo_width())
            idx = min(self.motor.cabezal, len(self.lblCeldas) - 1)
            lbl = self.lblCeldas[idx]
            xLbl = lbl.winfo_rootx() - self.marcoCinta.winfo_rootx()
            wLbl = lbl.winfo_width()
            xIzq = self.canvas.canvasx(0)
            if xLbl < xIzq + margen:
                nuevoIzq = max(0, xLbl - margen)
                self.canvas.xview_moveto(nuevoIzq / anchoTotal)
            elif xLbl + wLbl > xIzq + anchoVista - margen:
                nuevoIzq = min(anchoTotal - anchoVista, xLbl + wLbl + margen - anchoVista)
                self.canvas.xview_moveto(max(0, nuevoIzq) / anchoTotal)
        except Exception:
            pass

    # Se inicia la simulación con la cadena que el usuario escribe.
    def iniciar(self):
        texto = self.cajaEntrada.get() or ""
        self.construirCintaInicial(texto)
        self.lblEstado.configure(text=f"q{self.motor.estado}", fg=COLORTEXTO)
        self.lblResultado.configure(text="", fg=COLORTEXTO)
        self.lblEsperado.configure(text="")
        self.dibujarCinta(self.motor.cinta)
        self.btnPaso.configure(state=tk.NORMAL)
        self.btnCorrer.configure(state=tk.NORMAL, text="Correr")
        self.btnReiniciar.configure(state=tk.NORMAL)

    # Se alterna entre correr automáticamente o pausar.
    def alternarCorrer(self):
        if not self.enEjecucion:
            self.enEjecucion = True
            self.btnCorrer.configure(text="Pausar")
            self.bucleCorrer()
        else:
            self.enEjecucion = False
            self.btnCorrer.configure(text="Correr")

    # Se ejecuta un bucle de pasos automáticos con una pequeña pausa.
    def bucleCorrer(self):
        if not self.enEjecucion:
            return
        if self.enRebobinado:
            self.animarRebobinado()
            return
        fin = self.pasoNucleo()
        if fin in ("accept", "reject", "halt"):
            self.enEjecucion = False
            if fin == "accept":
                self.enRebobinado = True
                self.after(180, self.animarRebobinado)
            return
        self.after(self.retrasoMs, self.bucleCorrer)

    # Se realiza un paso manual cuando el usuario presiona el botón.
    def paso(self):
        if self.enRebobinado:
            self.animarRebobinado()
            return
        fin = self.pasoNucleo()
        if fin == "accept":
            self.enRebobinado = True
            self.after(180, self.animarRebobinado)

    # Se conecta el paso visual con el motor y se actualiza la interfaz.
    def pasoNucleo(self):
        oldHead = self.motor.cabezal
        resultado = self.motor.paso()

        # Actualiza la celda que acaba de ser procesada (si procede)
        if oldHead < len(self.motor.cinta) and oldHead < len(self.lblCeldas):
            nuevoTexto = self.motor.cinta[oldHead]
            color = COLORPROC if nuevoTexto == EPSILON else COLORTEXTO
            self.lblCeldas[oldHead].configure(text=nuevoTexto, fg=color)

        self.lblEstado.configure(text=f"q{self.motor.estado}", fg=COLORTEXTO)

        if resultado == "reject":
            # ¿rechazó por símbolo inesperado o por fin de cadena en estado no final?
            fin_cadena = (self.motor.cabezal == len(self.motor.cinta))
            esperados = self.motor.esperadosDesde(self.motor.estado)

            if fin_cadena:
                # Rechazo por terminar sin estar en estado final.
                if not esperados:
                    # No hay transiciones desde aquí: el fin de cadena no es válido en este estado.
                    self.mostrarEsperado([BLANCO], nota="(fin de cadena no permitido aquí)")
                else:
                    # Había transiciones posibles: faltó al menos un símbolo.
                    self.mostrarEsperado(esperados, nota="(faltó símbolo; no puede terminar aquí)")
            else:
                # Rechazo por símbolo no contemplado desde el estado actual.
                self.mostrarEsperado(esperados)

            self.lblResultado.configure(text="RECHAZADO", fg=COLORERROR)
            self.resaltarCabezal()
            return "reject"

        if resultado == "accept":
            self.lblEstado.configure(text=f"q{self.motor.estado} (final)", fg=COLOROK)
            self.lblResultado.configure(text="ACEPTADO (volviendo al principio)", fg=COLOROK)
            self.lblEsperado.configure(text="")
            self.resaltarCabezal()
            return "accept"

        # Paso normal
        self.lblEsperado.configure(text="")
        self.resaltarCabezal()
        return "ok"

    # Arma el texto bonito para los símbolos esperados.
    def formatearEsperados(self, simbolos):
        if not simbolos:
            return "—"
        partes = [f"'{s}'" for s in simbolos]
        if len(partes) == 1:
            return partes[0]
        return " o ".join(partes)

    # Muestra el mensaje "Se esperaba un: ..." bajo la cinta (con nota opcional).
    def mostrarEsperado(self, simbolos, nota=None):
        msg = self.formatearEsperados(simbolos)
        if nota:
            msg = f"{msg}  {nota}"
        self.lblEsperado.configure(text=f"Se esperaba un: {msg}", fg=COLORERROR)

    # Se anima el rebobinado cuando la cadena es aceptada.
    def animarRebobinado(self):
        if not self.enRebobinado:
            return
        if self.motor.cabezal > 0:
            self.motor.cabezal -= 1
            self.resaltarCabezal()
            self.after(70, self.animarRebobinado)
        else:
            self.enRebobinado = False
            self.lblResultado.configure(text="ACEPTADO", fg=COLOROK)
            self.lblEstado.configure(text=f"q{self.motor.estado} (final)", fg=COLOROK)
            self.btnCorrer.configure(state=tk.DISABLED)
            self.btnPaso.configure(state=tk.DISABLED)
