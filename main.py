'''
Agente Inteligente para Busca de Tesouro
Equipe:
- Dhiego Vinicius da Costa
- Emilieny de Souza Silva
- Marino Paulino Mouzinho da Silva

Inspirado no mundo de Wumpus e baseado no algoritmo A* para encontrar o tesouro em um ambiente desconhecido, com indicadores de tesouro, obstaculos e poços ao redor.
'''

from ambiente import Ambiente
from agente import Agente
import time
import os

def main():
    # Inicializa informações dos agentes: nome e posição inicial
    agentes_info = [("Agente 1", (0, 0)), ("Agente 2", (0, 1))]
    # Cria o ambiente com tamanho 10x10 e os agentes definidos
    ambiente = Ambiente(10, 10, agentes_info=agentes_info)
    # Instancia os objetos Agente para cada agente definido
    agentes = [
        Agente(ambiente, nome="Agente 1", posicao_inicial=(0, 0)),
        Agente(ambiente, nome="Agente 2", posicao_inicial=(0, 1))
    ]

    # Mostra o ambiente completo antes de iniciar a busca
    print("Ambiente inicial (Visão global):")
    ambiente.mostrar_grid_atual(visao_total=True)

    # Aguarda o usuário pressionar Enter para começar
    input("\nPressione Enter para iniciar a busca...")
    # Limpa o terminal antes de iniciar a simulação
    os.system("cls" if os.name == "nt" else "clear")
    tic = 0  # Contador de tics (passos)
    encontrou_tesouro = False  # Flag para indicar se algum agente encontrou o tesouro
    morreu = [False for _ in agentes]  # Lista para controlar se algum agente morreu

    # Loop principal da simulação: continua até encontrar o tesouro, todos morrerem ou atingir 100 tics
    while not encontrou_tesouro and not all(morreu) and tic < 100:
        tic += 1  # Incrementa o contador de tics
        for idx, agente in enumerate(agentes):
            if morreu[idx]:
                continue  # Pula agentes mortos
            os.system("cls" if os.name == "nt" else "clear")  # Limpa o terminal antes do movimento de cada agente

            # Agente decide sua próxima ação (posição para onde vai)
            proxima_pos = agente.decidir_proxima_acao()
            # Move o agente no ambiente e recebe o resultado da ação
            resultado = ambiente.mover_agente(proxima_pos, agente=agente)
            # Atualiza a posição do agente
            agente.posicao = ambiente.agente_posicoes[agente.nome]

            # Exibe informações do tic e do movimento do agente
            print(f"\n--- Tic {tic} ---")
            print(f"{agente.nome} moveu para: {proxima_pos}")
            ambiente.mostrar_grid_atual(visao_total=False)

            # Verifica o resultado do movimento
            if resultado == "TESOURO":
                print(f"\n{agente.nome} ENCONTROU O TESOURO!")
                encontrou_tesouro = True
                break  # Encerra o loop se o tesouro foi encontrado
            elif resultado == "MORTO":
                print(f"\n{agente.nome} MORREU! Caiu em um poço.")
                morreu[idx] = True  # Marca o agente como morto

            time.sleep(0.5)  # Pausa para facilitar visualização

    # Caso nenhum agente encontre o tesouro e todos estejam mortos ou o tempo acabe
    if not encontrou_tesouro and not any(morreu):
        print("\nTempo esgotado! Nenhum agente encontrou o tesouro.")

    # Mostra o mapa completo ao final da simulação
    print("\nMapa completo:")
    ambiente.mostrar_grid_atual(visao_total=True)

if __name__ == "__main__":
    main()