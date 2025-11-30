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

    # Símbolos de um caractere usados como literais
    literals = {':', ';', '[', ']', ',', '='}

    # Ignora espaços, tabs e carriage return
    ignore = ' \t\r'

    # Comentários de linha (opcional, não está no enunciado, mas ajuda)
    @_(r'//.*')
    def COMMENT(self, t):
        pass

    # Quebras de linha
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    # Números inteiros (NUM: inteiro não negativo)
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # Operadores lógicos: >, <, >=, <=, ==, !=
    @_(r'>=|<=|==|!=|>|<')
    def OPLOGIC(self, t):
        return t

    # Seta "->"
    @_(r'->')
    def ARROW(self, t):
        return t

    # Strings de mensagem: " ... "
    # Aceita caracteres comuns e escapes simples.
    @_(r'"([^"\\]|\\.)*"')
    def MSG(self, t):
        # Mantém as aspas na string; o parser decide o que fazer com elas
        return t

    # Identificadores e palavras-chave
    # ID_OBS e ID_DEVICE do enunciado viram todos o mesmo token ID aqui.
    @_(r'[A-Za-z_][A-Za-z0-9_]*')
    def ID(self, t):
        lex = t.value

        # Palavras-chave (case-insensitive quando faz sentido)
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
        # BOOL: True/False (qualquer combinação de maiúsculas/minúsculas)
        elif re.fullmatch(r'true', kw):
            t.type = 'BOOL'
            t.value = 'True'
        elif re.fullmatch(r'false', kw):
            t.type = 'BOOL'
            t.value = 'False'
        else:
            # continua como ID
            t.type = 'ID'

        return t

    # Tratamento de erro léxico
    def error(self, t):
        print(f'Caractere ilegal {t.value[0]!r} na linha {self.lineno}')
        self.index += 1
