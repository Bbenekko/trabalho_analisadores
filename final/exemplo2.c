#include <stdio.h>

#include "funcoes.h"

int movimento = 0;
int potencia = 0;
int umidade = 0;

int main(void)
{
    potencia = 100;
    if (umidade < 40) {
        alerta("Monitor", " Ar seco detectado ");
    }
    if (movimento == 1) {
        ligar("Lampada");
    } else {
        desligar("Lampada");
    }
    return 0;
}

