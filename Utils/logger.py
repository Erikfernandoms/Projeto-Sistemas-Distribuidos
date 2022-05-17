import os
import time


# ====== Ferramenta de logging
def logging(stop_signal, **componentes):
    while not stop_signal():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        '''Reatores'''
        print("{:^30} | {:^10} | {:^6} | Produtos".format("Processo", "Nível", "Ciclos"))
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

       
        time.sleep(0.5)
