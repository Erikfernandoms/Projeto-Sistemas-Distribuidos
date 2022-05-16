import os
import time

# ====== Ferramenta de logging
def logging(stop_signal, **components):
    while not stop_signal():
        os.system('cls' if os.name == 'nt' else 'clear')

        # Inputs
        print("{:^20} | {:^10} | Ciclos".format("Input", "Total injetado no sistema"))
        for input in components.get('inputs', []):
            print(input)
        print("\n\n")

        # Reactors
        print("{:^30} | {:^10} | {:^10} | {:^6} | Products".format("Reator", "Capacidade", "Nível", "Ciclos"))
        for r in components.get('reactors', []):
            print(r)
        print("\n\n")

        # Decanters
        print("{:^30} | {:^10} | {:^10} | {:^6} | Products".format("Decantador", "Capacidade", "Nível", "Ciclos"))
        for decanter in components.get('decanters', []):
            print(decanter)
        print("\n\n")

        # Dryers
        print("{:^30} | {:^10} | {:^10} | {:^6} | {:^17} | Drying".format("Secador", "Capacidade", "Nível", "Ciclos", "Products"))
        for dryer in components.get('dryers', []):
            print(dryer)
        print("\n\n")

        # Tanks
        print("{:^30} | {:^10} | {:^10} | {:^6} | Products".format("Tanques", "Capacidade", "Nível", "Ciclos"))
        for tank in components.get('tanks', []):
            print(tank)

        time.sleep(0.5)
        
        
    print("Finished executing...")
    print("Stoping threads...")
