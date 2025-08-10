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
    agentes_info = [("Agente 1", (0, 0)), ("Agente 2", (0, 1))]
    ambiente = Ambiente(10, 10, agentes_info=agentes_info)
    agentes = [
        Agente(ambiente, nome="Agente 1", posicao_inicial=(0, 0)),
        Agente(ambiente, nome="Agente 2", posicao_inicial=(0, 1))
    ]

    print("Ambiente inicial (Visão global):")
    ambiente.mostrar_grid_atual(visao_total=True)

    input("\nPressione Enter para iniciar a busca...")
    os.system("cls" if os.name == "nt" else "clear")
    tic = 0
    encontrou_tesouro = False
    morreu = [False for _ in agentes]

    while not encontrou_tesouro and not all(morreu) and tic < 100:
        tic += 1
        for idx, agente in enumerate(agentes):
            if morreu[idx]:
                continue
            os.system("cls" if os.name == "nt" else "clear")  # Limpa antes do movimento de cada agente
            proxima_pos = agente.decidir_proxima_acao()
            resultado = ambiente.mover_agente(proxima_pos, agente=agente)
            agente.posicao = ambiente.agente_posicoes[agente.nome]

            print(f"\n--- Tic {tic} ---")
            print(f"{agente.nome} moveu para: {proxima_pos}")
            ambiente.mostrar_grid_atual(visao_total=False)

            if resultado == "TESOURO":
                print(f"\n{agente.nome} ENCONTROU O TESOURO!")
                encontrou_tesouro = True
                break
            elif resultado == "MORTO":
                print(f"\n{agente.nome} MORREU! Caiu em um poço.")
                morreu[idx] = True

            time.sleep(0.5)
    # Se quiser limpar só a cada tic, mantenha o os.system fora do loop dos agentes

    if not encontrou_tesouro and not any(morreu):
        print("\nTempo esgotado! Nenhum agente encontrou o tesouro.")

    print("\nMapa completo:")
    ambiente.mostrar_grid_atual(visao_total=True)

if __name__ == "__main__":
    main()