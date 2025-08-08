import heapq
import math

class Agente:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.posicao = ambiente.agente_pos
        self.fronteira = []
        self.visitados = set([self.posicao])
        self.caminho = []
        self.conhecimento = {}  # Mapa do conhecimento do agente sobre o ambiente
        self.conhecimento[self.posicao] = ' '  # Posição inicial é livre

        # Prioridades para escolha de movimento (quanto menor, melhor)
        self.prioridade = {
            'T': 0,    # Tesouro - máxima prioridade
            '+': 1,    # Indício de tesouro
            '±': 2,    # Indício misto
            ' ': 3,    # Espaço livre
            '-': 4,    # Indício de poço
            'P': 5,    # Poço (deve ser evitado)
            'X': 6     # Obstáculo (não pode mover)
        }

    def atualizar_percepcoes(self):
        """Atualiza o conhecimento do agente com base nas percepções atuais"""
        percepcoes = self.ambiente.get_percepcao(self.posicao)
        for pos, conteudo in percepcoes.items():
            self.conhecimento[pos] = conteudo

    def decidir_proxima_acao(self):
        """Decide qual a próxima ação do agente usando A*"""
        self.atualizar_percepcoes()

        # Se o tesouro está nas percepções, vá direto para ele
        for pos, conteudo in self.conhecimento.items():
            if conteudo == 'T':
                return pos

        # Se não, use A* para encontrar o melhor caminho
        caminho = self.busca_a_estrela()
        if caminho and len(caminho) > 1:
            return caminho[1]  # O próximo passo no caminho
        else:
            # Se não encontrar caminho, tente mover para uma célula adjacente segura
            return self.movimento_seguro()

    def movimento_seguro(self):
        """Encontra um movimento seguro quando não há caminho claro"""
        vizinhos = self.get_vizinhos_validos(self.posicao)
        melhor_movimento = None
        menor_prioridade = float('inf')

        for vizinho in vizinhos:
            conteudo = self.conhecimento.get(vizinho, ' ')
            prioridade = self.prioridade.get(conteudo, 3)

            if prioridade < menor_prioridade and conteudo not in ['P', 'X']:
                menor_prioridade = prioridade
                melhor_movimento = vizinho

        return melhor_movimento if melhor_movimento else self.posicao

    def busca_a_estrela(self):
        """Implementa o algoritmo A* para encontrar o tesouro"""
        inicio = self.posicao
        fronteira = []
        heapq.heappush(fronteira, (0, inicio))
        veio_de = {}
        custo_ate_agora = {inicio: 0}

        while fronteira:
            _, atual = heapq.heappop(fronteira)

            # Se encontramos o tesouro, reconstrua o caminho
            if self.conhecimento.get(atual, ' ') == 'T':
                caminho = [atual]
                while atual in veio_de:
                    atual = veio_de[atual]
                    caminho.append(atual)
                caminho.reverse()
                return caminho

            for vizinho in self.get_vizinhos_validos(atual):
                novo_custo = custo_ate_agora[atual] + self.get_custo_movimento(vizinho)

                if vizinho not in custo_ate_agora or novo_custo < custo_ate_agora[vizinho]:
                    custo_ate_agora[vizinho] = novo_custo
                    prioridade = novo_custo + self.heuristica(vizinho)
                    heapq.heappush(fronteira, (prioridade, vizinho))
                    veio_de[vizinho] = atual

        return []  # Se não encontrar caminho

    def heuristica(self, posicao):
        """Heurística para A*: distância de Manhattan até o tesouro mais próximo conhecido"""
        # Primeiro, verifica se conhecemos a posição do tesouro
        for pos, conteudo in self.conhecimento.items():
            if conteudo == 'T':
                return abs(pos[0] - posicao[0]) + abs(pos[1] - posicao[1])

        # Se não conhece o tesouro, busca por indícios de tesouro
        min_dist = float('inf')
        for pos, conteudo in self.conhecimento.items():
            if conteudo in ['+', '±']:  # Indícios de tesouro
                dist = abs(pos[0] - posicao[0]) + abs(pos[1] - posicao[1])
                if dist < min_dist:
                    min_dist = dist

        return min_dist if min_dist != float('inf') else 0

    def get_custo_movimento(self, posicao):
        """Retorna o custo de se mover para uma posição"""
        conteudo = self.conhecimento.get(posicao, ' ')
        if conteudo == 'P' or conteudo == 'X':
            return float('inf')  # Custo infinito para poços e obstáculos
        elif conteudo == '-':
            return 10  # Alto custo para indícios de poço
        elif conteudo == '±':
            return 5   # Custo médio para indícios mistos
        elif conteudo == '+':
            return 1   # Baixo custo para indícios de tesouro
        else:
            return 1   # Custo padrão para espaços livres

    def get_vizinhos_validos(self, posicao):
        """Retorna vizinhos válidos para movimento"""
        x, y = posicao
        vizinhos = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.ambiente.n and 0 <= ny < self.ambiente.m:
                vizinhos.append((nx, ny))
        return vizinhos