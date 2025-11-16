# trabalho_analisadores

Para criar um arquivo yacc, o sufixo é ".y"
Para executar, basta:
``` yacc -d meu_programa.y ```
Isso irá gerar um arquivo y.tab.c

Para criar um arquivo lexico, o sufixo é ".l"
Para executar, basta:
``` lex lexer.l ```
Isso irá gerar um arquivo lex.yy.c

Para compila-lo, basta:
``` gcc y.tab.c lex.yy.c -o prgrama ```
e depois
``` ./programa ```