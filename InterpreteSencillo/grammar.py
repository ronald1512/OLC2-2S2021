# --------------------
# Ronald Romero
# --------------------

from Abstract.Objeto import TipoObjeto
import os
import re
from TS.Excepcion import Excepcion
import sys

sys.setrecursionlimit(3000)

errores = []
reservadas = {
    'println'   : 'RPRINT',
    'if'        : 'RIF',
    'else'      : 'RELSE',
    'while'     : 'RWHILE',
    'true'      : 'RTRUE',
    'false'     : 'RFALSE',
    'break'     : 'RBREAK',
    'function'  : 'RFUNC',
    'return'    : 'RRETURN',
}

tokens  = [
    'PUNTOCOMA',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'COMA',
    'MAS',
    'MENOS',
    'POR',
    'MENORQUE',
    'MAYORQUE',
    'IGUALIGUAL',
    'IGUAL',
    'AND',
    'OR',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PUNTOCOMA     = r';'
t_PARA          = r'\('
t_PARC          = r'\)'
t_LLAVEA        = r'{'
t_LLAVEC        = r'}'
t_COMA          = r','
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_MENORQUE      = r'<'
t_MAYORQUE      = r'>'
t_IGUALIGUAL    = r'=='
t_IGUAL         = r'='
t_AND           = r'&&'
t_OR            = r'\|\|'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t):
     r'[a-zA-Z][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')
     return t

def t_CADENA(t):
    r'(\".*?\")'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    errores.append(Excepcion("Lexico","Error léxico: " + t.value[0] , t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','MENORQUE','MAYORQUE', 'IGUALIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR'),
    )

# Definición de la gramática

#Abstract
from Abstract.NodoAST import NodoAST
from Instrucciones.Imprimir import Imprimir
from Expresiones.Constante import Constante
from Objeto.Primitivo import Primitivo
from TS.Tipo import OperadorAritmetico, OperadorLogico, OperadorRelacional
from Expresiones.Aritmetica import Aritmetica
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Expresiones.Identificador import Identificador
from Instrucciones.Asignacion import Asignacion
from Instrucciones.If import If
from Instrucciones.While import While
from Instrucciones.Break import Break
from Instrucciones.Funcion import Funcion
from Instrucciones.Llamada import Llamada
from Instrucciones.Return import Return

def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_instrucciones_instruccion(t) :
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]
    
#///////////////////////////////////////INSTRUCCIONES//////////////////////////////////////////////////

def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:    
        t[0] = [t[1]]

#///////////////////////////////////////INSTRUCCION//////////////////////////////////////////////////

def p_instruccion(t) :
    '''instruccion      : imprimir_instr PUNTOCOMA
                        | asignacion_instr PUNTOCOMA
                        | if_instr
                        | while_instr
                        | break_instr PUNTOCOMA
                        | funcion_instr
                        | llamada_instr PUNTOCOMA
                        | return_instr PUNTOCOMA'''
    t[0] = t[1]

def p_instruccion_error(t):
    'instruccion        : error PUNTOCOMA'
    errores.append(Excepcion("Sintáctico","Error Sintáctico:" + str(t[1].value) , t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""
#///////////////////////////////////////IMPRIMIR//////////////////////////////////////////////////

def p_imprimir(t) :
    'imprimir_instr     : RPRINT PARA expresion PARC'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))


#///////////////////////////////////////DECLARACIÓN Y ASIGNACION//////////////////////////////////////////////////

def p_asignacion(t) :
    'asignacion_instr     : ID IGUAL expresion'
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////IF//////////////////////////////////////////////////

def p_if1(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))

def p_if2(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE LLAVEA instrucciones LLAVEC'
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))

def p_if3(t) :
    'if_instr     : RIF PARA expresion PARC LLAVEA instrucciones LLAVEC RELSE if_instr'
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////WHILE//////////////////////////////////////////////////

def p_while(t) :
    'while_instr     : RWHILE PARA expresion PARC LLAVEA instrucciones LLAVEC'
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////BREAK//////////////////////////////////////////////////

def p_break(t) :
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////FUNCION//////////////////////////////////////////////////

def p_funcion_1(t) :
    'funcion_instr     : RFUNC ID PARA parametros PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))

def p_funcion_2(t) :
    'funcion_instr     : RFUNC ID PARA PARC LLAVEA instrucciones LLAVEC'
    t[0] = Funcion(t[2], [], t[6], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS//////////////////////////////////////////////////

def p_parametros_1(t) :
    'parametros     : parametros COMA parametro'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametros_2(t) :
    'parametros    : parametro'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO//////////////////////////////////////////////////

def p_parametro(t) :
    'parametro     : ID'
    t[0] = {'identificador':t[1]}

#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_llamada1(t) :
    'llamada_instr     : ID PARA PARC'
    t[0] = Llamada(t[1], [], t.lineno(1), find_column(input, t.slice[1]))

def p_llamada2(t) :
    'llamada_instr     : ID PARA parametros_llamada PARC'
    t[0] = Llamada(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////PARAMETROS LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametrosLL_1(t) :
    'parametros_llamada     : parametros_llamada COMA parametro_llamada'
    t[1].append(t[3])
    t[0] = t[1]
    
def p_parametrosLL_2(t) :
    'parametros_llamada    : parametro_llamada'
    t[0] = [t[1]]

#///////////////////////////////////////PARAMETRO LLAMADA A FUNCION//////////////////////////////////////////////////

def p_parametroLL(t) :
    'parametro_llamada     : expresion'
    t[0] = t[1]

#///////////////////////////////////////LLAMADA A FUNCION//////////////////////////////////////////////////

def p_return(t) :
    'return_instr     : RRETURN expresion'
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))

#///////////////////////////////////////EXPRESION//////////////////////////////////////////////////

def p_expresion_binaria(t):
    '''
    expresion : expresion MAS expresion
            | expresion MENOS expresion
            | expresion POR expresion
            | expresion MENORQUE expresion
            | expresion MAYORQUE expresion
            | expresion IGUALIGUAL expresion
            | expresion AND expresion
            | expresion OR expresion
    '''
    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1],t[3], t.lineno(2), find_column(input, t.slice[2]))


def p_expresion_agrupacion(t):
    '''
    expresion :   PARA expresion PARC 
    '''
    t[0] = t[2]

def p_expresion_llamada(t):
    '''expresion : llamada_instr'''
    t[0] = t[1]

def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Constante(Primitivo(TipoObjeto.ENTERO,t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Constante(Primitivo(TipoObjeto.DECIMAL, t[1]), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_cadena(t):
    '''expresion : CADENA'''
    t[0] = Constante(Primitivo(TipoObjeto.CADENA,str(t[1]).replace('\\n', '\n')), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_true(t):
    '''expresion : RTRUE'''
    t[0] = Constante(Primitivo(TipoObjeto.BOOLEANO, True), t.lineno(1), find_column(input, t.slice[1]))

def p_expresion_false(t):
    '''expresion : RFALSE'''
    t[0] = Constante(Primitivo(TipoObjeto.BOOLEANO, False), t.lineno(1), find_column(input, t.slice[1]))
 

import ply.yacc as yacc
parser = yacc.yacc()

from TS.Arbol import Arbol
from TS.TablaSimbolos import TablaSimbolos

def getErrores():
    return errores

def parse(inp) :
    global errores
    global lexer
    global parser
    errores = []
    lexer = lex.lex(reflags= re.IGNORECASE)
    parser = yacc.yacc()
    global input
    input = inp
    instrucciones=parser.parse(inp)
    ast = Arbol(instrucciones)
    TSGlobal = TablaSimbolos()
    ast.setTSglobal(TSGlobal)
    # for error in errores:                   # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    #     ast.getExcepciones().append(error)
    #     ast.updateConsola(error.toString())

    for instruccion in ast.getInstrucciones():
        if isinstance(instruccion, Funcion):
            ast.addFuncion(instruccion)
        # Aqui agregar demás validaciones (return, break o continue en lugar incorrecto)
        else:
            instruccion.interpretar(ast,TSGlobal)


    return ast;




