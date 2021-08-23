from Abstract.NodoReporteArbol import NodoReporteArbol
from TS.Simbolo import Simbolo
from Instrucciones.Funcion import Funcion
from Abstract.NodoAST import NodoAST
from TS.Excepcion import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Llamada(NodoAST):
    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.fila = fila
        self.columna = columna
    
    def interpretar(self, tree, table):
        result = tree.getFuncion(self.nombre.lower()) ## OBTENER LA FUNCION
        if result == None: # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "NO SE ENCONTRO LA FUNCION: " + self.nombre, self.fila, self.columna)
        nuevaTabla = TablaSimbolos(tree.getTSGlobal())
        # OBTENER PARAMETROS
        if len(result.parametros) != len(self.parametros): #LA CANTIDAD DE PARAMETROS ES LA ADECUADA
            return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
        contador=0
        for expresion in self.parametros: # SE OBTIENE EL VALOR DEL PARAMETRO EN LA LLAMADA
            resultExpresion = expresion.interpretar(tree, table)
            if isinstance(resultExpresion, Excepcion): return resultExpresion
            simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(), self.fila, self.columna, resultExpresion)
            resultTabla = nuevaTabla.setTabla(simbolo)
            if isinstance(resultTabla, Excepcion): return resultTabla
            contador += 1
        value = result.interpretar(tree, nuevaTabla)         # INTERPRETAR EL NODO FUNCION
        if isinstance(value, Excepcion): return value        
        return value

    def getNodo(self):
        nodo = NodoReporteArbol("LLAMADA A FUNCION")
        nodo.agregarHijo(str(self.nombre))
        parametros = NodoReporteArbol("PARAMETROS")
        for param in self.parametros:
            parametros.agregarHijoNodo(param.getNodo())
        nodo.agregarHijoNodo(parametros)
        return nodo