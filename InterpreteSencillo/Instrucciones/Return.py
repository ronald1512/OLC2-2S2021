from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos

class Return(NodoAST):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        result = self.expresion.interpretar(tree, table)
        if isinstance(result, Excepcion): return result
        self.result = result            #VALOR DEL RESULT
        return self

    def getNodo(self):
        nodo = NodoReporteArbol("RETURN")

        nodo.agregarHijoNodo(self.expresion.getNodo())

        return nodo