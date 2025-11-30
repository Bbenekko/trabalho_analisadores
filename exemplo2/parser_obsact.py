# parser_obsact.py
from sly import Parser
from lexer_obsact import ObsLexer


class ObsParser(Parser):
    tokens = ObsLexer.tokens

    def __init__(self):
        self.lexer = ObsLexer()
        # conjunto de variáveis observáveis (ID_OBS conceituais)
        self.obs_vars = set()

    # helper de identação
    def _indent(self, code, level=1):
        prefix = "    " * level
        lines = code.splitlines()
        return "\n".join(prefix + ln if ln.strip() else "" for ln in lines)

    # PROGRAM → DEV_SEC CMD_SEC EOF  (EOF é implícito no SLY)
    @_('dev_sec cmd_sec')
    def program(self, p):
        prelude = (
            "/* Código C gerado a partir de ObsAct */\n"
            "#include <stdio.h>\n\n"
            '#include "funcoes.h"\n\n'
        )

        globals_code = ""
        for name in sorted(self.obs_vars):
            globals_code += f"int {name} = 0;\n"
        if globals_code:
            globals_code += "\n"

        main_body = p.cmd_sec

        c_code = (
            prelude +
            globals_code +
            "int main(void)\n{\n" +
            self._indent(main_body) +
            "\n    return 0;\n}\n"
        )
        return c_code

    # DEV_SEC → dispositivos : DEV_LIST fimdispositivos
    @_('DISPOSITIVOS ":" dev_list FIMDISPOSITIVOS')
    def dev_sec(self, p):
        return ""

    # DEV_LIST → DEVICE DEV_LIST_TAIL
    @_('device dev_list_tail')
    def dev_list(self, p):
        return None

    # DEV_LIST_TAIL → DEVICE DEV_LIST_TAIL | ε
    @_('device dev_list_tail')
    def dev_list_tail(self, p):
        return None

    @_('')
    def dev_list_tail(self, p):
        return None

    # DEVICE → ID OPT_OBS
    @_('ID opt_obs')
    def device(self, p):
        # p.ID é o ID_DEVICE conceitual
        return None

    # OPT_OBS → [ ID ] | ε   (ID aqui é ID_OBS conceitual)
    @_('"[" ID "]"')
    def opt_obs(self, p):
        self.obs_vars.add(p.ID)
        return p.ID

    @_('')
    def opt_obs(self, p):
        return None

    # CMD_SEC → CMD_LIST
    @_('cmd_list')
    def cmd_sec(self, p):
        return p.cmd_list

    # CMD_LIST → CMD ; CMD_LIST_TAIL
    @_('cmd ";" cmd_list_tail')
    def cmd_list(self, p):
        tail = p.cmd_list_tail
        if tail:
            return p.cmd + "\n" + tail
        else:
            return p.cmd

    # CMD_LIST_TAIL → CMD ; CMD_LIST_TAIL | ε
    @_('cmd ";" cmd_list_tail')
    def cmd_list_tail(self, p):
        tail = p.cmd_list_tail
        if tail:
            return p.cmd + "\n" + tail
        else:
            return p.cmd

    @_('')
    def cmd_list_tail(self, p):
        return ""

    # CMD → ATTRIB | OBSACT | ACT
    @_('attrib')
    def cmd(self, p):
        return p.attrib

    @_('obsact')
    def cmd(self, p):
        return p.obsact

    @_('act')
    def cmd(self, p):
        return p.act

    # ATTRIB → def ID = VAL   (ID aqui é ID_OBS conceitual)
    @_('DEF ID "=" val')
    def attrib(self, p):
        self.obs_vars.add(p.ID)
        return f"{p.ID} = {p.val};"

    # OBSACT → quando OBS : ACT
    # OBSACT → quando OBS : ACT senao ACT
    @_('QUANDO obs ":" act')
    def obsact(self, p):
        inner = self._indent(p.act)
        return f"if ({p.obs}) {{\n{inner}\n}}"

    @_('QUANDO obs ":" act SENAO act')
    def obsact(self, p):
        then_part = self._indent(p.act0)
        else_part = self._indent(p.act1)
        return (
            f"if ({p.obs}) {{\n{then_part}\n}} else {{\n{else_part}\n}}"
        )

    # OBS → SIMPLE_OBS OBS_TAIL
    @_('simple_obs obs_tail')
    def obs(self, p):
        return p.simple_obs + p.obs_tail

    # OBS_TAIL → AND OBS | ε
    @_('AND obs')
    def obs_tail(self, p):
        return f" && {p.obs}"

    @_('')
    def obs_tail(self, p):
        return ""

    # SIMPLE_OBS → ID OPLOGIC VAL  (ID aqui é ID_OBS conceitual)
    @_('ID OPLOGIC val')
    def simple_obs(self, p):
        self.obs_vars.add(p.ID)
        return f"{p.ID} {p.OPLOGIC} {p.val}"

    # VAL → NUM | BOOL
    @_('NUM')
    def val(self, p):
        return str(p.NUM)

    @_('BOOL')
    def val(self, p):
        # BOOL foi lido como "True"/"False" no lexer
        if str(p.BOOL).lower() == 'true':
            return "1"
        else:
            return "0"

    # ACT regras:

    # ACT → execute ACTION em ID
    @_('EXECUTE action EM ID')
    def act(self, p):
        return f'{p.action}("{p.ID}");'

    # ACT → alerta para ID : MSG
    @_('ALERTA PARA ID ":" MSG')
    def act(self, p):
        return f'alerta("{p.ID}", {p.MSG});'

    # ACT → alerta para ID : MSG , ID   (último ID é ID_OBS conceitual)
    @_('ALERTA PARA ID ":" MSG "," ID')
    def act(self, p):
        self.obs_vars.add(p.ID1)
        return f'alerta_var("{p.ID0}", {p.MSG}, {p.ID1});'

    # ACT → difundir : MSG -> [ DEV_LIST_N ]
    @_('DIFUNDIR ":" MSG ARROW "[" dev_list_n "]"')
    def act(self, p):
        lines = [
            f'alerta("{dev}", {p.MSG});'
            for dev in p.dev_list_n
        ]
        return "\n".join(lines)

    # ACT → difundir : MSG ID -> [ DEV_LIST_N ]
    @_('DIFUNDIR ":" MSG ID ARROW "[" dev_list_n "]"')
    def act(self, p):
        self.obs_vars.add(p.ID)
        lines = [
            f'alerta_var("{dev}", {p.MSG}, {p.ID});'
            for dev in p.dev_list_n
        ]
        return "\n".join(lines)

    # ACTION → ligar | desligar
    @_('LIGAR')
    def action(self, p):
        return "ligar"

    @_('DESLIGAR')
    def action(self, p):
        return "desligar"

    # DEV_LIST_N → ID DEV_LIST_N_TAIL
    @_('ID dev_list_n_tail')
    def dev_list_n(self, p):
        return [p.ID] + p.dev_list_n_tail

    # DEV_LIST_N_TAIL → , ID DEV_LIST_N_TAIL | ε
    @_('"," ID dev_list_n_tail')
    def dev_list_n_tail(self, p):
        return [p.ID] + p.dev_list_n_tail

    @_('')
    def dev_list_n_tail(self, p):
        return []

    # Erro sintático
    def error(self, p):
        if p:
            print(f"Erro de sintaxe: token inesperado {p.type} ({p.value!r}) "
                  f"na linha {p.lineno}")
        else:
            print("Erro de sintaxe: fim de arquivo inesperado")
