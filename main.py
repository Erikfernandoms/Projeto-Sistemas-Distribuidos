from Processos.decantador import Decanter
from Processos.reator import Reactor
from Processos.secador import Dryer
from Processos.tanque_lavagem import WashTank
from Processos.tanque import Tank
from Utils.entrada import Input
from Utils.logger import logging
from Utils.gerenciador import Manager
from Utils.sinais import stop_signal
from env import *
import threading
import math


threads = []


'''Realizando a inserção dos produtos Oleo, NaOh, EtOH'''
input_oil = Input("Oleo", MIN_QTD_OLEO, MAX_QTD_OLEO, MIN_TEMPO_OLEO, MAX_TEMPO_OLEO, stop_signal)
input_NaOH = Input("NaOH", MIN_QTD_NAOH, MAX_QTD_NAOH, MIN_TEMPO_NAOH, MAX_TEMPO_NAOH, stop_signal)
input_EtOH = Input("EtOH", MIN_QTD_ETOH, MAX_QTD_ETOH, MIN_TEMPO_ETOH, MAX_TEMPO_ETOH, stop_signal)

'''Instanciando todos os tanques do sistema'''
tank_oil = Tank(math.inf, "Tanque - oleo", stop_signal)
tank_naoh_etoh = Tank(math.inf, "Tanque - NaOH/EtOH", stop_signal)
tank_glycerin = Tank(math.inf, "Tanque - Glicerina", stop_signal)
tank_biodisel = Tank(math.inf, "Tanque - Biodisel", stop_signal)
tank_etoh = Tank(math.inf, "Tanque - EtOH (Reaproveitado)", stop_signal)

'''Instanciando o reator que irá processar os produtos'''
reactor = Reactor(math.inf, "Reator", 5, stop_signal)

'''Instanciando o decantador que irá processar os produtos'''
decanter = Decanter(10, "Decantador", stop_signal)

'''Instanciando a lavagem com a perda de 7.5%'''
washing_tank_1 = WashTank(math.inf, "Lavagem 1", 0.075, stop_signal)
washing_tank_2 = WashTank(math.inf, "Lavagem 2", 0.075, stop_signal)
washing_tank_3 = WashTank(math.inf, "Lavagem 3", 0.075, stop_signal)

'''Instanciando os secadores'''
dryer_etoh = Dryer(math.inf, "Secador - EtOH", stop_signal, 0.03, 5)
dryer_biodisel = Dryer(math.inf, "Secador - Lavagem", stop_signal, 0.03, 5)

'''Realizando a comunicação dentre os processos, a função manager gerencia o que entra, sai e os logs desses processos'''
manage_oil_tank = Manager("Pipe(Oleo)", tank_oil)
manage_naoh_tank = Manager("Pipe(NaOH)", tank_naoh_etoh)
manage_etoh_tank = Manager("Pipe(EtOH)", tank_naoh_etoh)
manage_oil_reactor = Manager("Pipe(Oleo)", reactor)
manage_naoh_etoh_reactor = Manager("Pipe(NaOH/EtOH)", reactor)
manage_reactor_decanter = Manager("Pipe(NaOh/2EtOH/Oleo)", decanter)
manage_decanter_dryer = Manager("Pipe(EtOH) decanter", dryer_etoh)
manage_decanter_glycerin = Manager("Pipe(Glicerina)", tank_glycerin)
manage_decanter_washing_tank_1 = Manager("Pipe(Lavagem)", washing_tank_1)
manage_washing_tank_1_washing_tank_2 = Manager("Pipe(Lavagem)", washing_tank_2)
manage_washing_tank_2_washing_tank_3 = Manager("Pipe(Lavagem)", washing_tank_3)
manage_washing_tank_3_dryer_biodisel = Manager("Pipe(Lavagem)", dryer_biodisel)
manage_dryer_etoh_tank = Manager("Pipe(EtOH)", tank_etoh)
manage_etoh_tank_naoh_etoh = Manager("Pipe(EtOH[R])",tank_naoh_etoh)
manage_dryer_biodisel_tank = Manager("Pipe(Biodisel)", tank_biodisel)

'''Conexão dos tubos com os inputs de produtos'''
input_oil.connect_pipe(manage_oil_tank)
input_NaOH.connect_pipe(manage_naoh_tank)
input_EtOH.connect_pipe(manage_etoh_tank)
tank_oil.connect_pipe(manage_oil_reactor)
tank_naoh_etoh.connect_pipe(manage_naoh_etoh_reactor)
reactor.connect_pipe(manage_reactor_decanter)
decanter.connect_etoh_pipe(manage_decanter_dryer)
decanter.connect_glycerin_pipe(manage_decanter_glycerin)
decanter.connect_wash_pipe(manage_decanter_washing_tank_1)
washing_tank_1.connect_pipe(manage_washing_tank_1_washing_tank_2)
washing_tank_2.connect_pipe(manage_washing_tank_2_washing_tank_3)
washing_tank_3.connect_pipe(manage_washing_tank_3_dryer_biodisel)
tank_etoh.connect_pipe(manage_etoh_tank_naoh_etoh)
dryer_etoh.connect_pipe(manage_dryer_etoh_tank)
dryer_biodisel.connect_pipe(manage_dryer_biodisel_tank)

'''Instanciando método de log'''
log_thread = threading.Thread(
    target=logging, 
    name="logging_tool", 
    args=([stop_signal]),
    kwargs={
            'inputs': [input_oil, input_NaOH, input_EtOH],
            'dryers': [dryer_etoh, dryer_biodisel],
            'reactors': [reactor],
            'decanters': [decanter],
            'tanks': [tank_oil, tank_naoh_etoh, tank_glycerin, tank_etoh, tank_biodisel],
            'washtanks': [washing_tank_1, washing_tank_2, washing_tank_3]          
            })

'''Ligando threads de cada processo'''
threads.append(input_oil.start())
threads.append(input_NaOH.start())
threads.append(input_EtOH.start())
threads.append(tank_oil.start())
threads.append(tank_naoh_etoh.start())
threads.append(reactor.start())
threads.append(decanter.start())
threads.append(washing_tank_1.start())
threads.append(washing_tank_2.start())
threads.append(washing_tank_3.start())
threads.append(dryer_biodisel.start())
threads.append(dryer_etoh.start())
threads.append(tank_etoh.start())
threads.append(log_thread.start())


for thread in threads:
    if thread: thread.join()