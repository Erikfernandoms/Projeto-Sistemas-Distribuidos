import os
import time


# ====== Ferramenta de logging
def logging(stop_signal, **componentes):
    while not stop_signal():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        '''Reatores'''
        print("{:^30} | {:^10} | {:^6} | Produtos".format("Processos", "Litros", "Ciclos"))
        for reatores in componentes.get('reactors', []):
            print(reatores)

        '''Decantadores'''
        for decantador in componentes.get('decanters', []):
            print(decantador)
        
        '''Secadores'''
        for secagem in componentes.get('dryers', []):
            print(secagem)

        '''Tanque'''
        for tanque in componentes.get('tanks', []):
            print(tanque)

        print()
        print("{:^30} | {:^10} | {:^10} | {:^6} | Produtos".format("Processos", "Litros", "Perda", "Ciclos"))
        '''Lavagem'''
        for washtank in componentes.get('washtanks', []):
            print(washtank)

       
        time.sleep(0.5)
