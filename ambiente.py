import heapq
from collections import defaultdict
import random

class Ambiente: 
    # Inicialização do ambiente
    def __init__(self, n=10, m=10, agentes_info=None):
        self.n = n
        self.m = m
        self.grid = self.gerar_grid_aleatorio()  # Gera o grid do ambiente
        self.agente_posicoes = {}  # Dicionário para armazenar a posição de cada agente
        if agentes_info is None:
            agentes_info = [("Agente 1", (0, 0))]
        for nome, pos in agentes_info:
            self.agente_posicoes[nome] = pos
        self.tesouro_pos = self.encontrar_tesouro()  # Guarda a posição do tesouro
        self.visitados = set([self.agente_posicoes["Agente 1"]])  # Guarda posições visitadas

    def gerar_grid_aleatorio(self):
        '''
        Função que gera o grid do ambiente a partir dos parâmetros n e m:
        - Adiciona o Tesouro em posição aleatória (n>1, m>=0)
        - Aplica os indicadores de tesouro (+) ao redor do tesouro
        - Adiciona de 1 a 3 poços (P) e aplica seus indicadores (-) ao redor
        - Adiciona de 4 a 6 obstáculos (X) aleatórios ao grid
        '''
        grid = [[' ' for _ in range(self.m)] for _ in range(self.n)]

        # Insere o tesouro aleatoriamente
        tesouro_pos = (random.randint(1, self.n-1), random.randint(0, self.m-1))
        grid[tesouro_pos[0]][tesouro_pos[1]] = 'T'

        # Insere indícios de tesouro nas 8 posições ao redor do tesouro
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = tesouro_pos[0] + dx 
                ny = tesouro_pos[1] + dy
                if 0 <= nx < self.n and 0 <= ny < self.m:
                    grid[nx][ny] = '+'

        # Insere poços aleatoriamente
        num_pocos = random.randint(1, 3)
        for _ in range(num_pocos):
            poco_pos = (random.randint(1, self.n-1), random.randint(1, self.m-1))
            while grid[poco_pos[0]][poco_pos[1]] != ' ':
                poco_pos = (random.randint(1, self.n-1), random.randint(1, self.m-1))
            grid[poco_pos[0]][poco_pos[1]] = 'P'

            # Insere indícios de poço nas 8 posições ao redor do poço
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx = poco_pos[0] + dx
                    ny = poco_pos[1] + dy
                    if 0 <= nx < self.n and 0 <= ny < self.m:
                        if grid[nx][ny] == ' ':
                            grid[nx][ny] = '-'
                        elif grid[nx][ny] == '+':
                            grid[nx][ny] = '-'
                        elif grid[nx][ny] == 'T':
                            grid[nx][ny] = 'T'
                        elif grid[nx][ny] == 'P':
                            grid[nx][ny] = 'P'
                        elif grid[nx][ny] == 'X':
                            grid[nx][ny] = 'X'
                        else:
                            grid[nx][ny] = '-'

            # Insere obstáculos aleatoriamente
            num_obstaculos = random.randint(0, 4)
            for _ in range(num_obstaculos):
                obstaculo_pos = (random.randint(0, self.n-1), random.randint(1, self.m-1))
                while grid[obstaculo_pos[0]][obstaculo_pos[1]] in  ['T', 'P', '+', '-']:
                    obstaculo_pos = (random.randint(0, self.n-1), random.randint(1, self.m-1))
                grid[obstaculo_pos[0]][obstaculo_pos[1]] = 'X'

        return grid

    def encontrar_tesouro(self):
        '''
        Função responsável por encontrar a posição do tesouro no grid
        '''
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 'T':
                    return (i, j)
        return (0, 0)

    def get_percepcao(self, pos):
        '''
        Retorna o conteúdo das células adjacentes (N, S, L, O) à posição informada
        '''
        x, y = pos
        percepcao = {}
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.n and 0 <= ny < self.m:
                percepcao[(nx, ny)] = self.grid[nx][ny]
        return percepcao

    def mover_agente(self, nova_pos, agente):
        '''
        Move o agente para a nova posição, se válida, e retorna o resultado da ação:
        - "MORTO" se caiu em poço
        - "TESOURO" se encontrou o tesouro
        - "OK" se movimento normal
        - "INVALIDO" se posição não é válida
        '''
        nome = agente.nome
        if not self.posicao_valida(nova_pos):
            return "INVALIDO"
        conteudo = self.grid[nova_pos[0]][nova_pos[1]]
        self.agente_posicoes[nome] = nova_pos
        if conteudo == "P":
            return "MORTO"
        elif conteudo == "T":
            return "TESOURO"
        else:
            return "OK"

    def mostrar_grid_atual(self, visao_total=False):
        '''
        Mostra o grid atual no terminal.
        Se visao_total=True, mostra todo o grid; caso contrário, mostra apenas posições visitadas.
        Exibe todos os agentes presentes em cada célula.
        '''
        for i in range(self.n):
            linha = ""
            for j in range(self.m):
                pos = (i, j)
                agentes_aqui = [nome for nome, p in self.agente_posicoes.items() if p == pos]
                if agentes_aqui:
                    linha += "[" + ",".join(a[0] for a in agentes_aqui) + "]"
                else:
                    # Mostra o conteúdo da célula
                    linha += " " + self.grid[i][j] + " "
            print(linha)
    
    def posicao_valida(self, pos):
        '''
        Verifica se a posição é válida (dentro dos limites e não é obstáculo)
        '''
        i, j = pos
        return 0 <= i < self.n and 0 <= j < self.m and self.grid[i][j] != "X"