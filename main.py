from ambiente import Ambiente

def main():
    ambiente = Ambiente(10,10)
    print("Ambiente inicial:")
    ambiente.mostrar_grid_atual()

if __name__ == "__main__":
  main()