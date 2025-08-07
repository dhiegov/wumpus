class Agente:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.posicao = ambiente.agente_pos
        self.fronteira = []
        self.visitados = set()
        self.caminho = []
        self.prioridade = {
            'T': 0,
            '+': 1,
            ' ': 2,
            '-': 3,
            'P': 4,
            'X': 5,
        }
