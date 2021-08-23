from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Excepcion import Excepcion
from Abstract.NodoAST import NodoAST
from TS.Simbolo import Simbolo


class Asignacion(NodoAST):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        if value.tipo==TipoObjeto.ERROR:
            return value;

        simbolo = Simbolo(self.identificador, self.fila, self.columna, value)

        result = table.actualizarTabla(simbolo)     # Si no se encuentra el simbolo, lo agrega 

        if isinstance(result,Excepcion): return result
        
        return None

    def getNodo(self):
        nodo = NodoReporteArbol("ASIGNACION")
        nodo.agregarHijo(str(self.identificador))
        nodo.agregarHijoNodo(self.expresion.getNodo())
        return nodo