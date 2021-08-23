from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO

class Imprimir(NodoAST):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)

        if isinstance(value, Excepcion) :
            return value

        tree.updateConsola(value.valor) #TODO: Actualizar singleton en su campo consola
        return None

    def getNodo(self):
        nodo = NodoReporteArbol("IMPRIMIR")
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo