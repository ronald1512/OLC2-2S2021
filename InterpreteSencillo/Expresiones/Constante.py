from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST

class Constante(NodoAST):
    def __init__(self, valor, fila, columna):
        self.valor = valor      # Esta será una instancia de la clase OBJETO
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self.valor

    def getNodo(self):
        nodo = NodoReporteArbol("CONSTANTE")
        nodo.agregarHijo(str(self.valor))
        return nodo
