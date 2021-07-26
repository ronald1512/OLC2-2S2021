/**
 * contador binario
 * 111 -> 7
 * 11 -> 3
 */

/* Definición Léxica */
%lex

%options case-insensitive

%%

";"                 return 'PTCOMA';

/* Espacios en blanco */
[ \r\t]+            {}
\n                  {}
[0]                 return 'CERO';
[1]                 return 'UNO';



<<EOF>>                 return 'EOF';

.                       { console.error('Este es un error léxico: ' + yytext + ', en la linea: ' + yylloc.first_line + ', en la columna: ' + yylloc.first_column); }
/lex

%start ini

%% /* Definición de la gramática */

ini
	: lista EOF
;

lista
    : instruccion lista
    | instruccion
	| error     { console.error('Este es un error sintáctico: ' + yytext + ', en la linea: ' + this._$.first_line + ', en la columna: ' + this._$.first_column); }
;

instruccion
    : a PTCOMA {
		console.log('El valor de la expresión es: ' + $1);
	}
;

a
	: a num     {$$=$1*2+$2;}
    | num       {$$=$1;}
;

num
    : CERO  {$$=Number($1);}
    | UNO   {$$=Number($1);}
;