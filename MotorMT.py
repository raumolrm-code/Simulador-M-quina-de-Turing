# MotorMT.py
# Este archivo define la clase que maneja la lógica interna de la MT.
# La clase no dibuja nada en pantalla; solo cambia datos y estados.
# La interfaz gráfica llama a esta clase para avanzar paso a paso.

class MotorMT:
    def __init__(self, especificacion=None):
        # Se guarda la especificación del lenguaje activo.
        self.especActual = especificacion
        # Se guarda la cinta como una lista de símbolos.
        self.cinta = []
        # Se guarda la posición del cabezal (índice en la cinta).
        self.cabezal = 0
        # Se guarda el estado actual (entero).
        self.estado = 0

    def cargarEspecificacion(self, especificacion):
        # Se cambia la especificación (lenguaje) que va a usar la MT.
        self.especActual = especificacion

    def reiniciarConCadena(self, cadena):
        # Se prepara la cinta con la cadena y se vuelve al estado inicial.
        if self.especActual is None:
            raise ValueError("No hay especificación cargada.")
        self.cinta = list(cadena)
        self.cabezal = 0
        self.estado = self.especActual["start_state"]

    def paso(self):
        """
        Se realiza un paso de la MT.
        Devuelve:
          "ok"     → la MT avanza normalmente
          "accept" → el cabezal está en blanco y el estado es de aceptación
          "reject" → no hay regla válida o blanco en estado no final
        """
        # Si el cabezal está justo después del último símbolo, está en blanco.
        if self.cabezal == len(self.cinta):
            if self.estado in self.especActual["accept_states"]:
                return "accept"
            else:
                return "reject"

        simbolo = self.cinta[self.cabezal]

        # Se busca una regla que coincida con (estado, símbolo leido).
        idx = -1
        estActua = self.especActual["estActua"]
        lecturas = self.especActual["lecturas"]
        for i in range(len(estActua)):
            if estActua[i] == self.estado and lecturas[i] == simbolo:
                idx = i
                break

        # Si no existe regla, la cadena se rechaza.
        if idx == -1:
            return "reject"

        # Si existe regla, se toma la acción indicada.
        escribir = self.especActual["escribeC"][idx]
        estadoSig = self.especActual["estsigui"][idx]
        mover = self.especActual["mueveCab"][idx]

        # Se escribe el nuevo símbolo (usualmente ε para marcar procesado).
        self.cinta[self.cabezal] = escribir
        # Se cambia de estado.
        self.estado = estadoSig
        # Se mueve el cabezal.
        self.cabezal += mover

        return "ok"

    def esperadosDesde(self, estado=None):
        """
        Se devuelve la lista de símbolos que tienen transición válida
        desde el estado indicado (o desde el estado actual si no se indica).
        """
        if self.especActual is None:
            return []
        if estado is None:
            estado = self.estado

        estActua = self.especActual["estActua"]
        lecturas = self.especActual["lecturas"]
        vistos = set()
        orden = []
        for i in range(len(estActua)):
            if estActua[i] == estado:
                ch = lecturas[i]
                if ch not in vistos:
                    vistos.add(ch)
                    orden.append(ch)
        return orden
