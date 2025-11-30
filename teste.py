from sly import Lexer, Parser


class MyLexer(Lexer):
    tokens = {
        # keywords
        'AND', 'QUANDO', 'SENAO', 'EXECUTE', 'LIGAR', 'DESLIGAR', 
        'ALERTA_PARA', 'DIFUNDIR', 'DEF', 'EM',
        'DISPOSITIVOS', 'FIMDISPOSITIVOS',

        # Identificadores e Valores
        'ID_DEVICE', 'ID_OBS', 'MSG', 
        'NUM', 'BOOL', 
        
        # Operadores
        'OPLOGIC',
        'ARROW'
    }

    literals = {
        ':', '[', ']', ';', '=', 
        ',', '>', '-' 
    }

    ALERTA_PARA = r'alerta\ para'

    ARROW = r'->'

    OPLOGIC = r'(<=|>=|==|!=|<|>)'

    def __init__(self):
        self.keywords = {
            'dispositivos': 'DISPOSITIVOS',
            'fimdispositivos': 'FIMDISPOSITIVOS',
            'def': 'DEF',
            'quando': 'QUANDO',
            'senao': 'SENAO',
            'execute': 'EXECUTE',
            'em': 'EM',
            'ligar': 'LIGAR', 
            'desligar': 'DESLIGAR',
            'difundir': 'DIFUNDIR', 
            'and': 'AND',
            'TRUE': 'BOOL',
            'FALSE': 'BOOL', 
        }

    ID_DEVICE = r'[a-zA-Z]+'

    def ID_DEVICE(self, t):
        t.type = self.keywords.get(t.value, 'ID_DEVICE')
        return t
    
    ID_OBS = r'[a-zA-Z][a-zA-Z0-9]*'

    MSG = r'\"([^\\"]|\\.)*\"' 

    NUM = r'\d+'

    ignore = ' \t'

    def error(self, t):
        print(f"Caractere ilegal '{t.value[0]}' na linha {self.lineno}")
        self.index += 1

    
"""

class MyParser(Parser):
    debugfile = "parser.out"
    tokens = MyLexer.tokens

    def error(self, t):
        print(f"Syntax error at '{t.value}'")

    @_(
        "numero mais S",
        "numero menos S",
        "numero vezes S",
        "numero dividido S",
        "numero",
    )
    def S(self, p):
        print(f"Parsing: {p.numero}")

        if len(p) == 1:
            return p.numero
        elif len(p) == 3:
            if p[1] == "+":
                return p.numero + p.S
            elif p[1] == "-":
                return p.numero - p.S
            elif p[1] == "*":
                return p.numero * p.S
            elif p[1] == "/":
                return p.numero / p.S


parser = MyParser()
lexer = MyLexer()

string_to_parse = "1 + 2 + 3"

print(parser.parse(lexer.tokenize(string_to_parse)))

"""