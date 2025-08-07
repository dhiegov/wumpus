import heapq
from collections import defaultdict
import random

class Ambiente: 
   # Inicialização do ambiente
   def __init__(self, n = 10, m = 10):
      self.n = n
      self.m = m
      self.grid = self.gerar_grid_aleatorio()
      self.agente_pos = (0,0)
      self.tesouro_pos = self.encontrar_tesouro()

   def gerar_grid_aleatorio(self):
      '''
         Função que gera o grid de ammbiente a partir do n, m passado na seguinte ordem:
         - Adiciona o Tesouro em posição n>1 e m>=0
         - Aplica os indicadores de tesouro ao redor da posicao do tesouro
         - Adiciona 1 a 3 poços e aplica seus indicadores ao redor de cada poço
         - Adiciona 4 à 10 obstaculos aleatorios ao grid
      '''

      #Gera o grid do ambiente
      grid = [[' ' for _ in range(self.m)] for _ in range(self.n)]

      #insere o tesouro aleatoriamente
      tesouro_pos = (random.int(1, self.n-1), random.int(0, self.m-1))
      grid[tesouro_pos[0]][tesouro_pos[1]] = 'T'

      #insere indices de 
      return grid

   def encontrar_tesouro(self):
      '''
         Função responsável por encontrar o tesouro disposto no grid
      '''
      return 0
   
   def get_percepcao(self, pos):
      '''
         Método responsável por retornar o conteúdo das células adjacentes à posição passada
      '''
      x,y = pos
      percepcao = {}
      for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
         nx, ny = x + dx, y + dy
         if 0 <= nx < self.n and 0 <= ny < self.m:
            percepcao[(nx, ny)] = self.grid[nx][ny]
      return percepcao

   def mover_agente(self, nova_pos):
      '''
         Método responsável por mover o agente no ambiente para nova posição e retorna o resultado
      '''
      if nova_pos == self.tesouro_pos:
         self.agente_pos = nova_pos
         return "TESOURO"
      
      if self.grid[nova_pos[0]][nova_pos[1]] == 'P':
         return "MORTO"
      
      if self.grid[nova_pos[0]][nova_pos[1]] == 'X':
         return "BLOQUEADO"
      
      self.agente_pos = nova_pos
      return "OK"

      
   def mostrar_grid_atual(self, visao_total = False):
      '''
         Método de exibição do ambiente atual
         - Visão Total = False: Apresenta o agente e revela o conteudo das posições já visitadas por ele
         - Visão Total = True: Apresenta o agente e o conteúdo de todas posições do ambiente, independente se foi visitado ou não
      '''
      header = [f' {i} ' for i in range(self.m)]
      print('    '.join(header))
      for i in range(self.n):
         linha=[]
         for j in range(self.m):
            if (i,j) == self.agente_pos:
               linha.append(" A ")
            elif visao_total: # TODO: Adicionar o fato do agente já ter visitado esta posição
               linha.append(" "+self.grid[i][j]+" ")
            else:
               linha.append(" ? ")
         print(f' {i} | '.join(linha))
  