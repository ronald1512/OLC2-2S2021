from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST


class Identificador(NodoAST):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        simbolo = table.getTabla(self.identificador.lower())

        if simbolo == None:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada.", self.fila, self.columna)
        
        return simbolo.getValor()

    def getNodo(self):
        nodo = NodoReporteArbol("IDENTIFICADOR")
        nodo.agregarHijo(str(self.identificador))
        return nodo