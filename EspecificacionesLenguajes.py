# EspecificacionesLenguajes.py
# Este archivo define:
#   1) Las constantes globales de la máquina de Turing.
#   2) La clase que construye las "especificaciones" de 10 lenguajes.
# Cada lenguaje se describe con 5 listas paralelas:
#   - estActua, lecturas, escribeC, estsigui, mueveCab
# Se usa un estilo sencillo para que se lea sin dificultad.

# --- Constantes globales MT ---
BLANCO   = "□"   # Símbolo visual de fin de cadena
EPSILON  = "ε"   # Marca visual de "ya procesado"

MOVERDER = 1     # Movimiento a la derecha
MOVERIZQ = -1    # Movimiento a la izquierda (se reserva)
MOVERNO  = 0     # Sin movimiento

class EspecificacionesLenguajes:
    # Esta función convierte un diccionario de reglas a las 5 listas.
    # Sirve para mantener un formato claro y uniforme.
    @staticmethod
    def aListas(delta):
        estActua, lecturas, escribeC, estsigui, mueveCab = [], [], [], [], []
        for (estado, leido), (escribir, estadoSig, mover) in delta.items():
            estActua.append(estado)
            lecturas.append(leido)
            escribeC.append(escribir)
            estsigui.append(estadoSig)
            mueveCab.append(mover)
        return estActua, lecturas, escribeC, estsigui, mueveCab

    # L1: (ab)*  → puede aceptar la vacía y repeticiones "ab".
    @staticmethod
    def specL1():
        delta = {
            (0, 'a'): (EPSILON, 1, MOVERDER),
            (1, 'b'): (EPSILON, 0, MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre": "L1: (ab)*", "start_state": 0, "accept_states": {0}, "alphabet": {'a','b'},
                "estActua":E, "lecturas":L, "escribeC":W, "estsigui":S, "mueveCab":M}

    # L2: a(a|b)*b  → empieza con 'a' y termina con 'b'.
    @staticmethod
    def specL2():
        delta = {
            (0,'a'):(EPSILON,1,MOVERDER),
            (1,'a'):(EPSILON,1,MOVERDER), (1,'b'):(EPSILON,2,MOVERDER),
            (2,'a'):(EPSILON,1,MOVERDER), (2,'b'):(EPSILON,2,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L2: a(a|b)*b","start_state":0,"accept_states":{2},"alphabet":{'a','b'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L3: 0*1*  → ceros seguidos de unos (la vacía también vale).
    @staticmethod
    def specL3():
        delta = {
            (0,'0'):(EPSILON,0,MOVERDER),
            (0,'1'):(EPSILON,1,MOVERDER),
            (1,'1'):(EPSILON,1,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L3: 0*1*","start_state":0,"accept_states":{0,1},"alphabet":{'0','1'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L4: a+b+c+  → al menos una 'a', luego una 'b', luego una 'c'.
    @staticmethod
    def specL4():
        delta = {
            (0,'a'):(EPSILON,1,MOVERDER),
            (1,'a'):(EPSILON,1,MOVERDER), (1,'b'):(EPSILON,2,MOVERDER),
            (2,'b'):(EPSILON,2,MOVERDER), (2,'c'):(EPSILON,3,MOVERDER),
            (3,'c'):(EPSILON,3,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L4: a+b+c+","start_state":0,"accept_states":{3},"alphabet":{'a','b','c'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L5: cadenas binarias que contienen la subcadena "101".
    @staticmethod
    def specL5():
        delta = {
            (0,'1'):(EPSILON,1,MOVERDER), (0,'0'):(EPSILON,0,MOVERDER),
            (1,'0'):(EPSILON,2,MOVERDER), (1,'1'):(EPSILON,1,MOVERDER),
            (2,'1'):(EPSILON,3,MOVERDER), (2,'0'):(EPSILON,0,MOVERDER),
            (3,'0'):(EPSILON,3,MOVERDER), (3,'1'):(EPSILON,3,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L5: contiene '101'","start_state":0,"accept_states":{3},"alphabet":{'0','1'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L6: número par de 'a' sobre {a,b}.
    @staticmethod
    def specL6():
        delta = {
            (0,'a'):(EPSILON,1,MOVERDER), (0,'b'):(EPSILON,0,MOVERDER),
            (1,'a'):(EPSILON,0,MOVERDER), (1,'b'):(EPSILON,1,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L6: #a par sobre {a,b}","start_state":0,"accept_states":{0},"alphabet":{'a','b'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L7: (1|0)*00  → termina exactamente en "00".
    @staticmethod
    def specL7():
        delta = {
            (0,'0'):(EPSILON,1,MOVERDER), (0,'1'):(EPSILON,0,MOVERDER),
            (1,'0'):(EPSILON,2,MOVERDER), (1,'1'):(EPSILON,0,MOVERDER),
            (2,'0'):(EPSILON,2,MOVERDER), (2,'1'):(EPSILON,0,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L7: termina en '00'","start_state":0,"accept_states":{2},"alphabet":{'0','1'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L8: longitud exacta 3 sobre {a,b,c}.
    @staticmethod
    def specL8():
        delta = {
            (0,'a'):(EPSILON,1,MOVERDER), (0,'b'):(EPSILON,1,MOVERDER), (0,'c'):(EPSILON,1,MOVERDER),
            (1,'a'):(EPSILON,2,MOVERDER), (1,'b'):(EPSILON,2,MOVERDER), (1,'c'):(EPSILON,2,MOVERDER),
            (2,'a'):(EPSILON,3,MOVERDER), (2,'b'):(EPSILON,3,MOVERDER), (2,'c'):(EPSILON,3,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L8: longitud=3 {a,b,c}","start_state":0,"accept_states":{3},"alphabet":{'a','b','c'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L9: a*b*c*  → primero a's, luego b's, luego c's (la vacía vale).
    @staticmethod
    def specL9():
        delta = {
            (0,'a'):(EPSILON,0,MOVERDER), (0,'b'):(EPSILON,1,MOVERDER), (0,'c'):(EPSILON,2,MOVERDER),
            (1,'b'):(EPSILON,1,MOVERDER), (1,'c'):(EPSILON,2,MOVERDER),
            (2,'c'):(EPSILON,2,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L9: a*b*c*","start_state":0,"accept_states":{0,1,2},"alphabet":{'a','b','c'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # L10: (a|b)*a  → cadenas sobre {a,b} que terminan en 'a'.
    @staticmethod
    def specL10():
        delta = {
            (0,'a'):(EPSILON,1,MOVERDER), (0,'b'):(EPSILON,0,MOVERDER),
            (1,'a'):(EPSILON,1,MOVERDER), (1,'b'):(EPSILON,0,MOVERDER),
        }
        E,L,W,S,M = EspecificacionesLenguajes.aListas(delta)
        return {"nombre":"L10: (a|b)*a (termina en 'a')","start_state":0,"accept_states":{1},"alphabet":{'a','b'},
                "estActua":E,"lecturas":L,"escribeC":W,"estsigui":S,"mueveCab":M}

    # Esta función devuelve la lista con los 10 lenguajes listos para usar.
    @staticmethod
    def obtenerLista():
        return [
            EspecificacionesLenguajes.specL1(),
            EspecificacionesLenguajes.specL2(),
            EspecificacionesLenguajes.specL3(),
            EspecificacionesLenguajes.specL4(),
            EspecificacionesLenguajes.specL5(),
            EspecificacionesLenguajes.specL6(),
            EspecificacionesLenguajes.specL7(),
            EspecificacionesLenguajes.specL8(),
            EspecificacionesLenguajes.specL9(),
            EspecificacionesLenguajes.specL10(),
        ]
