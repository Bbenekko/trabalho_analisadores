#include <stdio.h>

#include "funcoes.h"

int temperatura = 0;

int main(void)
{
    temperatura = 30;
    ligar("lampada");
    if (temperatura > 25) {
        alerta("ventilador", "Muito quente!");
    }
    return 0;
}

