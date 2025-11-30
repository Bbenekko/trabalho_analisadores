# main.py

from lexer import MyLexer
from nao_funciona.parser import MyParser
# from code_generator import CodeGenerator # Em uma fase futura

def compile_obsact(source_code):
    """Executa a análise léxica e sintática."""
    
    # 1. Inicializa Lexer e Parser
    lexer = MyLexer()
    parser = MyParser()
    
    try:
        # 2. Executa a análise léxica e passa os tokens para o parser
        tokens = list(lexer.tokenize(source_code))
        
        print("--- Tokens Gerados ---")
        for tok in tokens:
            print(tok)
            
        print("\n--- Análise Sintática ---")
        ast = parser.parse(iter(tokens)) # Passa o iterador de tokens
        
        print("\nAST (Árvore de Sintaxe Abstrata):")
        # Use o pprint para visualizar a estrutura da AST
        from pprint import pprint
        pprint(ast)
        
        # 3. FASE FUTURA: Geração de Código
        # code_generator = CodeGenerator()
        # output_code = code_generator.generate(ast)
        # return output_code

    except Exception as e:
        print(f"\nERRO NO PROCESSO DE COMPILAÇÃO: {e}")
        return None

if __name__ == '__main__':
    # Código de teste na linguagem ObsAct
    TEST_CODE = """
dispositivos:
    Termometro [temperatura]
    Ventilador
fimdispositivos

def temperatura = 40;
def potencia = 90;

quando temperatura > 30 AND potencia <= 100 execute ligar em Ventilador;
"""
    print("Iniciando Compilação do Programa ObsAct...\n")
    
    # Roda a função principal
    compile_obsact(TEST_CODE)
    
    # Se estivesse gerando código:
    # final_program = compile_obsact(TEST_CODE)
    # if final_program:
    #     print("\n--- CÓDIGO FINAL GERADO (Exemplo Python) ---")
    #     print(final_program)