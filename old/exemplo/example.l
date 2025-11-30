/* Exemplo de arquivo flex */

%{
    // C stuff (headers, declaration, variables, etc) 

    #include <stdio.h>
    #include <stdlib.h>
    #include "example.tab.h" // importantísimo
    
    void printError();
    int a;
%}
/* Após esse bloco, os comentários devem ser assim*/

/* Expressões regulares */
/* Exemplo */
numbers ([0-9])+
alpha ([a-zA-Z])+

/*Especificações de token */
/*Exemplo */
/* NÃO ACEITA COMENTáRIOS */
%%

{alpha}			   {sscanf(yytext, "%s", yylval.name); return (STRING);}
{numbers}      {yylval.number = atoi(yytext); return (NUM);}
";"      		   {return (SEMICOLON);}
.      		     {printError(); return(OTHER);}

%%

/* Funções em C */
/* Exemplo */
void printError()
{
    printf("Erro!");
}
/* NECESSÁRIO */
int yywrap()
{
    return 1;
}