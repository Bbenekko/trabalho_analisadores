# trabalho_analisadores

Para criar um arquivo yacc, o sufixo é ".y".
Para executar, basta:
``` 
bison -d meu_programa.y 
```
Isso irá gerar um arquivo y.tab.c
<br>
<br>
Para criar um arquivo lexico, o sufixo é ".l".
Para executar, basta:
``` 
flex lexer.l 
```
Isso irá gerar um arquivo lex.yy.c.
<br>
<br>
Para compila-lo, basta:
``` 
gcc meu_programa.tab.c lex.yy.c -o prgrama -lfl
```
e depois
``` 
./programa 
```