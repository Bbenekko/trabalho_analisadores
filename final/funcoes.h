void ligar(char* id_device)
{
    printf("%s ligado!\n", id_device); 
}

void desligar(char* id_device)
{
    printf("%s desligado!\n", id_device); 
}

void alerta(char* id_device, char* msg)
{
    printf("%s recebeu o alerta:\n%s\n", id_device, msg); 
}

void alerta_var(char* id_device, char* msg, int var)
{
    printf("%s recebeu o alerta:\n%s %d\n", id_device, msg, var); 
}
