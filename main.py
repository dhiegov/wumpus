from ambiente import Ambiente
from agente import Agente

def main():
    ambiente = Ambiente(10,10)
    #agente = Agente(ambiente)
    print("Ambiente inicial (VIsão global):")
    ambiente.mostrar_grid_atual(visao_total=True )
      


if __name__ == "__main__":
  main()