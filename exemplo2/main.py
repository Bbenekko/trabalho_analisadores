# main.py
import sys
from lexer_obsact import ObsLexer
from parser_obsact import ObsParser


def main():
    # Lê a entrada: arquivo passado na linha de comando
    #   python main.py programa.obs > programa.c
    # ou, sem argumento, lê de stdin:
    #   python main.py < programa.obs > programa.c
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = sys.stdin.read()

    lexer = ObsLexer()
    parser = ObsParser()

    # Tokeniza e faz o parse
    tokens = lexer.tokenize(data)
    c_code = parser.parse(tokens)

    if c_code is not None:
        print(c_code)
    else:
        print("Nenhum código foi gerado (erro de análise?).", file=sys.stderr)


if __name__ == "__main__":
    main()
