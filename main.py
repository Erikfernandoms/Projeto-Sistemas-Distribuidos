from multiprocessing import Process
from time import sleep

from tanque_oleo import Tanque_Oleo

def orquestrador():
    while True:
        sleep(10)
        tanque_oleo = Tanque_Oleo(10)
        print(tanque_oleo())
    
if __name__ == '__main__':
    orquestrador()