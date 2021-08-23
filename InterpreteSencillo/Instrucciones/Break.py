from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST

class Break(NodoAST):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNodo(self):
        nodo = NodoReporteArbol("BREAK")
        return nodo