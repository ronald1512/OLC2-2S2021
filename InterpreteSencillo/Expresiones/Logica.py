from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorLogico

class Logica(NodoAST):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna

    
    def interpretar(self, tree, table):
        res_left = self.OperacionIzq.interpretar(tree, table)
        res_right = self.OperacionDer.interpretar(tree, table)

        if(res_left.tipo == TipoObjeto.ERROR):
            return res_left;
        if(res_right.tipo == TipoObjeto.ERROR):
            return res_right;  

        if (self.operador==OperadorLogico.OR):
            return Primitivo(TipoObjeto.BOOLEANO, bool(str(res_left.getValue())) or bool(str(res_right.getValue())));
        
        if (self.operador==OperadorLogico.AND):
            return Primitivo(TipoObjeto.BOOLEANO, bool(str(res_left.getValue())) and bool(str(res_right.getValue())));
        
        return Excepcion(TipoObjeto.ERROR, f"Operador desconocido: {self.operador}",self.fila,self.columna);

            
        

    def getNodo(self):
        nodo = NodoReporteArbol("LOGICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo