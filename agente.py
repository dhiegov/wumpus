import heapq
import random
from collections import defaultdict

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
            ' ': 2,    # Espaço livre
            '-': 3,    # Indício de poço
            'P': 4,    # Poço (deve ser evitado)
            'X': 5     # Obstáculo (não pode mover)
        }

    def atualizar_percepcoes(self):
        """Atualiza o conhecimento do agente com base nas percepções atuais"""
        percepcoes = self.ambiente.get_percepcao(self.posicao)
        for pos, conteudo in percepcoes.items():
            self.conhecimento[pos] = conteudo

    def decidir_proxima_acao(self):
        """Decide qual a próxima ação do agente usando A* com prevenção de loops"""
        self.atualizar_percepcoes()

        # Verifica se tesouro está visível
        for pos, conteudo in self.conhecimento.items():
            if conteudo == 'T':
                return pos

        # Busca caminho com A* modificado
        caminho = self.busca_a_estrela()

        if caminho and len(caminho) > 1:
            proxima_pos = caminho[1]

            # Verifica se a próxima posição é segura
            conteudo = self.conhecimento.get(proxima_pos, ' ')
            if conteudo not in ['P', 'X']:
                return proxima_pos

        # Fallback: movimento seguro com prevenção de loops
        return self.movimento_seguro_com_evitacao()

    def movimento_seguro_com_evitacao(self):
        """Encontra movimento seguro evitando posições problemáticas"""
        vizinhos = self.get_vizinhos_validos(self.posicao)
        melhor_movimento = None
        menor_custo = float('inf')

        for vizinho in vizinhos:
            conteudo = self.conhecimento.get(vizinho, ' ')
            custo = (
                self.prioridade.get(conteudo, 3) +
                self.evitar_loops(vizinho) +
                random.uniform(0, 0.5)  # Aleatoriedade para variar
            )

            if custo < menor_custo and conteudo not in ['P', 'X']:
                menor_custo = custo
                melhor_movimento = vizinho

        return melhor_movimento if melhor_movimento else self.posicao

    def busca_a_estrela(self):
        """Implementa o algoritmo A* para encontrar o tesouro com prevenção de loops"""
        inicio = self.posicao
        fronteira = []
        heapq.heappush(fronteira, (0, inicio))
        veio_de = {}
        custo_ate_agora: dict[tuple[int, int], float] = {inicio: 0}

        # Dicionário para contar quantas vezes cada posição foi visitada
        contagem_visitas = defaultdict(int)
        contagem_visitas[inicio] += 1

        while fronteira:
            _, atual = heapq.heappop(fronteira)

            if self.conhecimento.get(atual, ' ') == 'T':
                caminho = [atual]
                while atual in veio_de:
                    atual = veio_de[atual]
                    caminho.append(atual)
                caminho.reverse()
                return caminho

            # Se visitou esta posição muitas vezes, pule para evitar loops
            if contagem_visitas[atual] > 2:
                continue

            for vizinho in self.get_vizinhos_validos(atual):
                conteudo = self.conhecimento.get(vizinho, ' ')

                # Penaliza revisitar posições
                penalidade = contagem_visitas[vizinho] * 2  # Aumenta custo para posições já visitadas

                novo_custo = custo_ate_agora[atual] + self.get_custo_movimento(vizinho) + penalidade

                if vizinho not in custo_ate_agora or novo_custo < custo_ate_agora[vizinho]:
                    contagem_visitas[vizinho] += 1
                    custo_ate_agora[vizinho] = novo_custo
                    prioridade = novo_custo + self.heuristica(vizinho)

                    # Adiciona um pequeno valor aleatório para quebrar empates
                    prioridade += random.uniform(0, 0.1)

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
            if conteudo in ['+']:  # Indícios de tesouro
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
            return 10.0  # Alto custo para indícios de poço
        elif conteudo == '+':
            return 1.0   # Baixo custo para indícios de tesouro
        else:
            return 5.0   # Custo padrão para espaços livres

    def get_vizinhos_validos(self, posicao):
        """Retorna vizinhos válidos para movimento"""
        x, y = posicao
        vizinhos = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.ambiente.n and 0 <= ny < self.ambiente.m:
                vizinhos.append((nx, ny))
        return vizinhos

    def evitar_loops(self, posicao):
        """Retorna uma penalidade baseada em quantas vezes a posição foi visitada"""
        if posicao in self.visitados:
            return 5 * len([p for p in self.visitados if p == posicao])
        return 0