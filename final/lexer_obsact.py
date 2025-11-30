from sly import Lexer
import re

class ObsLexer(Lexer):
    # Lista de tokens
    tokens = {
        'NUM', 'BOOL', 'MSG', 'ID',
        'OPLOGIC', 'AND', 'ARROW',
        'DISPOSITIVOS', 'FIMDISPOSITIVOS',
        'DEF', 'QUANDO', 'SENAO',
        'EXECUTE', 'EM',
        'ALERTA', 'PARA',
        'DIFUNDIR',
        'LIGAR', 'DESLIGAR',
    }

    literals = {':', ';', '[', ']', ',', '='}

    # Ignorar espaços e tabs
    ignore = ' \t\r'

    # Quebras de linha
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    # Números inteiros não negativos!
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # Operadores lógicos: >, <, >=, <=, ==, !=
    @_(r'>=|<=|==|!=|>|<')
    def OPLOGIC(self, t):
        return t

    # Setinha "->"
    @_(r'->')
    def ARROW(self, t):
        return t

    # Strings de mensagem: " ... "
    @_(r'"([^"\\]|\\.)*"')
    def MSG(self, t):
        # Mantém as aspas na string!!
        return t

    # Identificadores e palavras-chave
    # Tem que começar com letras e depois pode ter letra ou dígito!!
    @_(r'[A-Za-z][A-Za-z0-9]*')
    def ID(self, t):
        lex = t.value
        kw = lex.lower()

        kw = lex.lower()
        if kw == 'dispositivos':
            t.type = 'DISPOSITIVOS'
        elif kw == 'fimdispositivos':
            t.type = 'FIMDISPOSITIVOS'
        elif kw == 'def':
            t.type = 'DEF'
        elif kw == 'quando':
            t.type = 'QUANDO'
        elif kw == 'senao':
            t.type = 'SENAO'
        elif kw == 'execute':
            t.type = 'EXECUTE'
        elif kw == 'em':
            t.type = 'EM'
        elif kw == 'alerta':
            t.type = 'ALERTA'
        elif kw == 'para':
            t.type = 'PARA'
        elif kw == 'difundir':
            t.type = 'DIFUNDIR'
        elif kw == 'and':
            t.type = 'AND'
        elif kw == 'ligar':
            t.type = 'LIGAR'
        elif kw == 'desligar':
            t.type = 'DESLIGAR'
        elif re.fullmatch(r'true', kw): # BOOL: True/False (qualquer combinação de maiúsculas/minúsculas)
            t.type = 'BOOL'
            t.value = 'True'
        elif re.fullmatch(r'false', kw):
            t.type = 'BOOL'
            t.value = 'False'
        else:
            # continua como ID
            t.type = 'ID'

        return t

    # Tratamento de erro
    def error(self, t):
        print(f'Caractere ilegal {t.value[0]!r} na linha {self.lineno}')
        self.index += 1
