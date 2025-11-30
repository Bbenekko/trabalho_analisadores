#include <stdio.h>

#include "funcoes.h"

int movimento = 0;
int potencia = 0;
int umidade = 0;

int main(void)
{
    umidade = 40;
    if (movimento == 1) 
    {
        ligar("Lampada");
    } 
    else 
    {
        if (umidade < 50) 
        {
            alerta("Monitor", " Ar seco detectado ");
        } 
        else 
        {
            alerta("Monitor", " Ar molhado detectado ");
        }
    }
    return 0;
}

