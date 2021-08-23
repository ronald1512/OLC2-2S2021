from Objeto.Primitivo import Primitivo
from Abstract.Objeto import TipoObjeto
from enum import Enum
from Abstract.NodoReporteArbol import NodoReporteArbol
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.Tipo import TIPO, OperadorAritmetico


class Aritmetica(NodoAST):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna


    def interpretar(self, tree, table):
        res_left = self.OperacionIzq.interpretar(tree, table)
        res_right = self.OperacionDer.interpretar(tree,table)

        if(res_left.tipo == TipoObjeto.ERROR):
            return res_left;
        if(res_right.tipo == TipoObjeto.ERROR):
            return res_right;  

        if (self.operador==OperadorAritmetico.MAS):
            if(res_left.tipo!=TipoObjeto.CADENA and res_right.tipo!=TipoObjeto.CADENA):
                return Primitivo(TipoObjeto.ENTERO, int(str(res_left.getValue())) + int(str(res_right.getValue())));
            return Primitivo(TipoObjeto.CADENA, str(res_left.getValue()) + str(res_right.getValue()));
        
        if (self.operador==OperadorAritmetico.MENOS):
            return Primitivo(TipoObjeto.ENTERO, int(str(res_left.getValue())) - int(str(res_right.getValue())));
        
        if (self.operador==OperadorAritmetico.POR):
            return Primitivo(TipoObjeto.ENTERO, int(str(res_left.getValue())) * int(str(res_right.getValue())));
        
        if (self.operador==OperadorAritmetico.DIV):
            return Primitivo(TipoObjeto.ENTERO, int(str(res_left.getValue())) / int(str(res_right.getValue())));
        
        return Excepcion(TipoObjeto.ERROR, f"Operador desconocido: {self.operador}",self.fila,self.columna);


    def getNodo(self):
        nodo = NodoReporteArbol("ARITMETICA")
        if self.OperacionDer != None:
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.agregarHijo(str(self.operador))
            nodo.agregarHijoNodo(self.OperacionIzq.getNodo())
        
        return nodo