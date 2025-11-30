#include <stdio.h>

#include "funcoes.h"

int umidade = 0;

int main(void)
{
    if (umidade < 40) {
        alerta("Monitor", " Ar seco detectado ");
    }
    return 0;
}

