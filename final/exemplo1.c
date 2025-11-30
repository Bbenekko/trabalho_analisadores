#include <stdio.h>

#include "funcoes.h"

int temperatura = 0;

int main(void)
{
    if (temperatura > 30) {
        alerta_var("Monitor", " Temperatura em ", temperatura);
        alerta_var("Celular", " Temperatura em ", temperatura);
    }
    return 0;
}

