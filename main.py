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
from os import system

def main():
    # Inicializa o ambiente e o agente
    ambiente = Ambiente(10, 10)
    agente = Agente(ambiente)

    print("Ambiente inicial (Visão global):")
    ambiente.mostrar_grid_atual(visao_total=True)

    input("\nPressione Enter para iniciar a busca...")
    system("clear")
    tic = 0
    encontrou_tesouro = False
    morreu = False

    while not encontrou_tesouro and not morreu and tic < 100:
        system("clear")
        tic += 1
        print(f"\n--- Tic {tic} ---")

        # Agente decide a próxima ação
        proxima_pos = agente.decidir_proxima_acao()

        # Executa a ação no ambiente
        resultado = ambiente.mover_agente(proxima_pos)
        agente.posicao = ambiente.agente_pos

        # Mostra o estado atual
        print(f"Agente moveu para: {proxima_pos}")
        ambiente.mostrar_grid_atual(visao_total=False)

        # Verifica resultados
        if resultado == "TESOURO":
            print("\n🎉🎉🎉 TESOURO ENCONTRADO! 🎉🎉🎉")
            encontrou_tesouro = True
        elif resultado == "MORTO":
            print("\n💀💀💀 AGENTE MORTO! Caiu em um poço. 💀💀💀")
            morreu = True

        time.sleep(0.5)  # Pequena pausa para visualização

    if not encontrou_tesouro and not morreu:
        print("\n⏰ Tempo esgotado! Agente não encontrou o tesouro.")

    # Mostra o mapa completo no final
    print("\nMapa completo:")
    ambiente.mostrar_grid_atual(visao_total=True)

if __name__ == "__main__":
    main()