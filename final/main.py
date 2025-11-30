import sys
from lexer_obsact import ObsLexer
from parser_obsact import ObsParser

def main():
    #   python main.py programa.obs > programa.c
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = f.read()
    else:
        data = sys.stdin.read()

    lexer = ObsLexer()
    parser = ObsParser()

    tokens = lexer.tokenize(data)
    c_code = parser.parse(tokens)

    if c_code is not None:
        print(c_code)
    else:
        print("ERRO: Nenhum código foi gerado.", file=sys.stderr)


if __name__ == "__main__":
    main()
