# Analizador Sintáctico Simple

José Ricardo Aguirre Villado
A01562775

## Para ejecutar el analizador
Utiliza python 3.11.2 y para ejecutar el código es de la siguiente forma 
`python3 main.py` sigue la misma estructura de archivos de carpeta inputs donde se reciben los mismos tokens generados por el analizador léxico y carpeta outputs con los datos necesarios para proximas actividades.


Este proyecto es para aprender como funciona un analizador sintactico en este caso (parser) para lenguaje mini C, como habiamos visto en la actividad anterior del análisis léxico.

Para definir la grámatica del analizador sintáctico se utiliza para organizarlo rápidamente y de forma estructurada EBNF (Extended Backus-Naur Form).
Este es mi EBNF para la actividad:

## EBNF

```ruby
program         ::= { statement }

statement       ::= declaration
                  | assignment
                  | while_loop
                  | for_loop

declaration     ::= type IDENTIFIER [ "=" expression ] ";"
assignment      ::= IDENTIFIER "=" expression ";"

while_loop      ::= "while" "(" expression ")" "{" { statement } "}"
for_loop        ::= "for" "(" declaration_no_semicolon ";" expression ";" update ")" "{" { statement } "}"

declaration_no_semicolon ::= type IDENTIFIER [ "=" expression ]

update          ::= IDENTIFIER "++"
                  | assignment

expression      ::= relational_expression
relational_expression ::= additive_expression { ("<" | ">") additive_expression }
additive_expression   ::= term { ("+" | "-") term }
term            ::= factor { ("*" | "/") factor }
factor          ::= NUMBER
                  | IDENTIFIER
                  | "(" expression ")"

type            ::= "int" | "float" | "char"

```

El programa esta separado en 3 archivos.
1. main.py Programa principal que ejecuta el resto del código
2. parser.py Clase parser y otras funciones para el analizador.
3. ast_nodes.py Todas las clases de AST (Abstract Syntax Tree)

