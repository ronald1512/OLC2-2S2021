

from TS.Excepcion import Excepcion


class TablaSimbolos:
    def __init__(self, anterior = None):
        self.tabla = {} # Diccionario Vacio
        self.anterior = anterior

    def setTabla(self, simbolo):      # Agregar una variable
        if simbolo.id.lower() in self.tabla :
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None

    def getTabla(self, id):            # obtener una variable
        tablaActual = self
        while tablaActual != None:
            if id.lower() in tablaActual.tabla :
                return tablaActual.tabla[id.lower()]           # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual != None:
            if simbolo.id.lower() in tablaActual.tabla :
                tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                return None             # simbolo actualizado
            else:
                tablaActual = tablaActual.anterior
        
        self.tabla[simbolo.id.lower()] = simbolo
        return None # --> simbolo agregado
        
    
