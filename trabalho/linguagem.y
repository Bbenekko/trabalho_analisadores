// Exemplo de arquivo Bison
%{
#include <stdio.h>

int yylex();
int yyerror(char *s);

%}

%token STRING NUM BOOL OTHER SEMICOLON

%union{
	char name[20];
    unsigned int number;
    bool boolean;
}


%type <name> STRING
%type <number> NUM
%type <boolean> BOOL

%%

prog:
  stmts
;

stmts:
		| stmt SEMICOLON stmts

stmt:
		STRING {
				printf("Your entered a string - %s", $1);
		}
		| NUM {
				printf("The number you entered is - %d", $1);
		}
		| OTHER
;

%%

int yyerror(char *s)
{
	printf("Syntax Error on line %s\n", s);
	return 0;
}

int main()
{
    yyparse();
    return 0;
}