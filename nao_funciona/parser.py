# parser.py

from sly import Parser
from lexer import MyLexer 

class MyParser(Parser):
    tokens = MyLexer.tokens
    
    # Precedência: AND deve ter a menor para avaliar a condição por último
    precedence = (
        ('left', 'AND'),
    )

    # ----------------------------------------
    # --- 1. Regra Principal: PROGRAM ---
    # PROGRAM → DEV_SEC CMD_SEC
    @_('DEV_SEC CMD_SEC')
    def PROGRAM(self, p):
        return ('program', p.DEV_SEC, p.CMD_SEC)

    # ----------------------------------------
    # --- 2. Seção de Dispositivos (DEV_SEC) ---
    # ----------------------------------------
    # DEV_SEC → dispositivos: DEV_LIST fimdispositivos
    @_('DISPOSITIVOS ":" DEV_LIST FIMDISPOSITIVOS')
    def DEV_SEC(self, p):
        return ('device_section', p.DEV_LIST)

    # DEV_LIST → DEVICE DEV_LIST | DEVICE
    @_('DEVICE DEV_LIST')
    def DEV_LIST(self, p):
        p.DEV_LIST.insert(0, p.DEVICE)
        return p.DEV_LIST
    
    @_('DEVICE')
    def DEV_LIST(self, p):
        return [p.DEVICE]

    # DEVICE → ID_DEVICE
    @_('ID_DEVICE')
    def DEVICE(self, p):
        return ('device', p.ID_DEVICE, None)

    # DEVICE → ID_DEVICE [ ID_OBS ]
    @_('ID_DEVICE "[" ID_OBS "]"')
    def DEVICE(self, p):
        return ('device_sensor', p.ID_DEVICE, p.ID_OBS)

    # ----------------------------------------
    # --- 3. Seção de Comandos (CMD_SEC) ---
    # ----------------------------------------

    # CMD_SEC → CMD_LIST
    @_('CMD_LIST')
    def CMD_SEC(self, p):
        return ('command_section', p.CMD_LIST)

    # CMD_LIST → CMD_LIST CMD ; | CMD ;
    @_('CMD_LIST CMD ";"')
    def CMD_LIST(self, p):
        p.CMD_LIST.append(p.CMD)
        return p.CMD_LIST

    @_('CMD ";"')
    def CMD_LIST(self, p):
        return [p.CMD]

    # CMD → ATTRIB | OBSACT | ACT (ACT puro é permitido, como em 'execute ligar em Lampada;')
    @_('ATTRIB')
    def CMD(self, p):
        return p[0]

    @_('OBSACT')
    def CMD(self, p):
        return p[0]
    
    @_('ACT') 
    def CMD(self, p):
        return p[0]

    # --- 3.1 ATTRIB (Atribuição/Definição) ---

    # ATTRIB → DEF ID_OBS = VAL
    @_('DEF ID_OBS "=" VAL')
    def ATTRIB(self, p):
        return ('attribute', p.ID_OBS, p.VAL)

    # --- 3.2 OBSACT (Observação e Ação) ---

    # OBSACT → QUANDO OBS ACT
    @_('QUANDO OBS ACT')
    def OBSACT(self, p):
        return ('obs_action', p.OBS, p.ACT, None)

    # OBSACT → QUANDO OBS ACT SENAO ACT
    @_('QUANDO OBS ACT SENAO ACT')
    def OBSACT(self, p):
        return ('obs_action_else', p.OBS, p.ACT0, p.ACT1)

    # --- 3.3 OBS (Condição de Observação) ---

    # OBS → ID_OBS OPLOGIC VAL
    @_('ID_OBS OPLOGIC VAL')
    def OBS(self, p):
        return ('condition', p.ID_OBS, p.OPLOGIC, p.VAL)
    
    # OBS → ID_OBS OPLOGIC VAL AND OBS
    @_('ID_OBS OPLOGIC VAL AND OBS')
    def OBS(self, p):
        # Cria a estrutura AND para condições compostas
        return ('compound_condition_and', 
                ('condition', p.ID_OBS, p.OPLOGIC, p.VAL), 
                p.OBS)

    # --- 3.4 VAL (Valores) ---

    # VAL → NUM | BOOL
    @_('NUM')
    def VAL(self, p):
        return ('value_num', p.NUM)

    @_('BOOL')
    def VAL(self, p):
        return ('value_bool', p.BOOL)

    # --- 3.5 ACTION (Ações Primitivas) ---

    # ACTION → LIGAR | DESLIGAR
    @_('LIGAR')
    def ACTION(self, p):
        return 'ligar'

    @_('DESLIGAR')
    def ACTION(self, p):
        return 'desligar'

    # --- 3.6 ACT (Execução, Alerta e Difusão) ---

    # ACT → EXECUTE ACTION EM ID_DEVICE
    @_('EXECUTE ACTION EM ID_DEVICE')
    def ACT(self, p):
        return ('execute_action', p.ACTION, p.ID_DEVICE)

    # ACT → ALERTA_PARA ID_DEVICE : MSG
    @_('ALERTA_PARA ID_DEVICE ":" MSG')
    def ACT(self, p):
        return ('alert_simple', p.ID_DEVICE, p.MSG)

    # ACT → ALERTA_PARA ID_DEVICE : MSG , ID_OBS
    @_('ALERTA_PARA ID_DEVICE ":" MSG "," ID_OBS')
    def ACT(self):
        # Alerta com concatenação: MSG + " " + ID_OBS (valor)
        return ('alert_concat', p.ID_DEVICE, p.MSG, p.ID_OBS)
        
    # ACT → DIFUNDIR : MSG > [ DEV_LIST_N ]
    @_('DIFUNDIR ":" MSG ">" "[" DEV_LIST_N "]"')
    def ACT(self, p):
        return ('diffuse_msg', p.MSG, p.DEV_LIST_N)

    # ACT → DIFUNDIR : MSG ID_OBS -> [ DEV_LIST_N ]
    @_('DIFUNDIR ":" MSG ID_OBS ARROW "[" DEV_LIST_N "]"')
    def ACT(self, p):
        return ('diffuse_concat', p.MSG, p.ID_OBS, p.DEV_LIST_N)

    # --- 3.7 DEV_LIST_N (Lista de dispositivos para difusão) ---

    # DEV_LIST_N → ID_DEVICE , DEV_LIST_N | ID_DEVICE
    @_('ID_DEVICE "," DEV_LIST_N')
    def DEV_LIST_N(self, p):
        p.DEV_LIST_N.insert(0, p.ID_DEVICE)
        return p.DEV_LIST_N

    @_('ID_DEVICE')
    def DEV_LIST_N(self, p):
        return [p.ID_DEVICE]

    def error(self, p):
        if p:
            print(f"Erro de sintaxe em '{p.type}' ({p.value}) na linha {p.lineno}")
        else:
            print("Erro de sintaxe no final do arquivo (EOF)")