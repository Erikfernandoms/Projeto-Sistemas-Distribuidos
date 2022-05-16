from .tanque import Tank
from env import DEBUG, TIME_MULTIPLIER
import time

class Reactor(Tank):
    def __init__(self, capacity, name, flow, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.flow = flow
        self.products = {
                        'NaOH': 0,
                        'Oleo': 0,
                        'EtOH': 0
                        }
        self.cumulated_output = 0

    def pump(self):
        # O Reator processa 5L/s, sendo: 1 parte NaOH, 1 parte Oleo e 2 partes EtOH
        # ou seja, para 5L, tem-se no maximo 1.25L de NaOH, 1.25L de Oleo e 2.5L de EtOh
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            with self.tanklock:
                # limita a transferencia no maximo por segundo
                naoh = min(self.flow/4, self.products['NaOH'])
                oil  = min(self.flow/4, self.products['Oleo'])
                etoh = min(self.flow/2, self.products['EtOH'])
                # encontra o gargalo
                products_limited = {'NaOH': naoh, 'Oleo': oil, 'EtOH': etoh/2}
                bottleneck = min(products_limited.keys(), key=(lambda product: products_limited[product]))
                next_iter = products_limited[bottleneck] == 0
            # Se nao tiver nada para enviar, só espera pela proxima iteração
            if next_iter: continue
            # dado o gargalo escolhe as quantidades que serao processadas
            if bottleneck == 'NaOH':
                used =  {
                    'NaOH': naoh,
                    'Oleo': naoh,
                    'EtOH': 2*naoh
                }
            elif bottleneck == 'Oleo':
                used =  {
                    'NaOH': oil,
                    'Oleo': oil,
                    'EtOH': 2*oil
                }
            elif bottleneck == 'EtOH':
                used =  {
                    'NaOH': etoh/2,
                    'Oleo': etoh/2,
                    'EtOH': etoh
                }
            else:
                raise Exception("Invalid Product on reactor")
            # Calcula o total utilizado
            total = sum(used.values())
            # Reduz do tanque a quantidade processada
            with self.tanklock:
                for product, amount in used.items():
                    # Gera o produto resultado
                    throwback = 0
                    for pipe in self.output_pipes:
                        # Assume-se que o throwback simplesmente vaza do reator
                        throwback += pipe(amount/len(self.output_pipes), "Mistura")
                    self.products[product] -= (amount + throwback)
                    self.cicles += 1
            # Adiciona o que saiu ao total acumulado e reduz o nivel do tanque
            self.cumulated_output += total
            self.level -= total
            # Para por 1 seg pois a vazao é considerada em L/s
            time.sleep(1*TIME_MULTIPLIER)
            # Descansa se necessario
            if self.cumulated_output > 3:
                # Calcula tempo de descanso - 5s para cada 3L de output
                rest_time = (5*3/self.cumulated_output)-1 # -1 pois ja descansa 1 segundo sempre
                time.sleep(rest_time*TIME_MULTIPLIER)
                self.cumulated_output = 0

    def __call__(self, qtt, product):
        with self.tanklock:
            # Calcula quanto entra no tanque (entry) e quanto volta pelo pile (throwback)
            entry = self.capacity-self.level if qtt + self.level > self.capacity else qtt
            throwback = qtt - entry
            # Adiciona no tanque
            self.level += entry
            self.products[product] += entry
            return throwback

    def __str__(self):
        with self.tanklock:
            products_string = ' / '.join(["{:.2f} ({})".format(amount, product_name).ljust(20, ' ') for product_name, amount in self.products.items()])
            status_string = "{:<30} | {:>10} | {:>10.2f} | {:<6} | ".format(self.name, self.capacity, self.level, self.cicles)
            status_string += products_string
        return status_string