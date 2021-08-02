# --------------------
# Ronald Romero
# --------------------

# primero definimos los nombres de los tokens
tokens = (
    'PARIZQ',
    'PARDER',
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'AND',
    'OR',
    'IGIG',
    'DIFDE',
    'MAY',
    'MEN',
    'DECIMAL',
    'ENTERO',
    'RTRUE',
    'RFALSE'
)

#para definir los patrones de los tokens podemos agregar
#el prefijo 't_'
#PARA ESPECIFICAR UNA EXPRESION REGULAR DEBEMOS HACER USO DE 'r'

t_PARIZQ = r'\('
t_PARDER = r'\)'
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_AND = r'&'
t_OR = r'\|'
t_IGIG = r'=='
t_DIFDE = r'!='
t_MAY = r'>'
t_MEN = r'<'
t_RTRUE=r'true'
t_RFALSE=r'false'

#Otra forma de definir patrones es con funciones:

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

#Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGIG', 'DIFDE'),
    ('nonassoc', 'MEN', 'MAY'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV'),
    ('right','UMENOS'),
    ('left','PARIZQ', 'PARDER'),
    )

# Definicion de la gramática
contTemp=1
contEtq=1
def newTemp():
    global contTemp
    cad = 'T'+str(contTemp)
    contTemp+=1
    return cad

def newEtq():
    global contEtq
    cad = 'L' + str(contEtq)
    contEtq+=1
    return cad


def p_expresion_l_1(t):
    '''l  :     l   OR  m'''
    lv=str(t[1][0])+', '+str(t[3][0])
    lf=str(t[3][1])
    t[0]=[lv, lf, str(t[1][2])+str(t[1][1])+ ':\r\n'+str(t[3][2])]

def p_expresion_l_2(t):
    'l  :   m'
    t[0]=t[1]

def p_expresion_m_1(t):
    'm  :   m   AND r'
    lv=str(t[3][0])
    lf=str(t[1][1])+ ', '+str(t[3][1])
    t[0]=[lv, lf, str(t[1][2]) + str(t[1][0]) + ':\r\n'+ str(t[3][2])]

def p_expresion_m_2(t):
    'm  :   r'
    t[0]=t[1]

def p_expresion_r_1(t):
    'r  :   e   MAY e'
    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, str(t[1][1])+str(t[3][1])+' if '+ str(t[1][0])+ ' > '+ str(t[3][0]) + ' goto '+lv+'\r\n'+' goto '+lf+'\r\n']


def p_expresion_r_2(t):
    'r  :   e   MEN e'

    lv=newEtq()
    lf=newEtq()
    cad=str(t[1][1])+str(t[3][1])+' if '+ str(t[1][0])+ ' < '+ str(t[3][0]) + ' goto '+lv+'\r\n'+' goto '+lf+'\r\n'
    #print(cad)
    t[0]=[lv, lf, cad]


def p_expresion_r_3(t):
    'r  :   e   IGIG e'
    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, str(t[1][1])+str(t[3][1])+' if '+ str(t[1][0])+ ' == '+ str(t[3][0]) + ' goto '+lv+'\r\n'+' goto '+lf+'\r\n']

def p_expresion_r_4(t):
    'r  :   e   DIFDE e'
    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, str(t[1][1])+str(t[3][1])+' if '+ str(t[1][0])+ ' != '+ str(t[3][0]) + ' goto '+lv+'\r\n'+' goto '+lf+'\r\n']

def p_expresion_r_5(t):
    'r  :   RTRUE'
    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, 'if 1 == 1 goto '+lv + '\r\n' +'goto '+lf+'\r\n']

def p_expresion_r_6(t):
    'r  :   RFALSE'

    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, 'if 1 == 0 goto '+lv + '\r\n' +'goto '+lf+'\r\n']


#NOTA:  antes de generar C3D se debe de validar que 'r' siempre tome valores booleanos pero para evitar esa validacion
#       por ser este un ejemplo pequeño, así que lo pongo asi.
def p_expresion_r_7(t):
    'r  :   e'

    lv=newEtq()
    lf=newEtq()
    t[0]=[lv, lf, str(t[1][1])]




def p_expresion_binaria(t):
    '''e  :     e   MAS     e
            |   e   MENOS   e
            |   e   POR     e
            |   e   DIV     e '''

    temp=newTemp()
    cad=str(t[1][1])+str(t[3][1])+temp+' = '+str(t[1][0])+t[2]+str(t[3][0])+'\r\n'
    #print(cad)
    t[0]=[temp, cad]

def p_expresion_unaria(t):
    '''e  :     MENOS   e   %prec   UMENOS'''
    temp=newTemp()
    t[0]=[temp, t[2][1]+temp+' = 0 - '+t[2][0]+'\r\n']

def p_expresion_agrupacion(t):
    'e : PARIZQ e PARDER'
    t[0]=t[2] #copio los list

def p_expresion_number(t):
    '''e    : ENTERO
            | DECIMAL'''
    t[0]=[t[1], ''] #creo un LIST de 2 elementos
    #print(t[0])
def p_error(t):
    print("Error sintáctico en '%s'" % str(t))

import ply.yacc as yacc
parser = yacc.yacc()

def parse(input):
    global contTemp
    global contEtq
    contTemp=1
    contEtq=1
    cad=parser.parse(input)
    return str(cad[2])+'\n'+str(cad[0])+':\r\n'+'ETIQUETA_VERDADERA'+'\r\n\n'+str(cad[1])+':\r\n'+'ETIQUETA_FALSA\r\n'





#ahora escribimos la salida en codigo 3 direcciones
# f = open ('salida.txt','w')
# f.write(salida)
# f.close()