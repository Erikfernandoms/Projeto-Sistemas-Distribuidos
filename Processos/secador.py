from .tanque import Tank
from env import DEBUG, TIME_MULTIPLIER
import time

class Dryer(Tank):
    def __init__(self, capacity, name, stop_signal, loss, time_per_liter):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss
        self.time_per_liter = time_per_liter
        self.drying_time = 0
        self.drying_liters = 0

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            if len(self.output_pipes) > 0:
                # Puxa o proximo da fila
                amount = 0.0
                product = None
                with self.tanklock:
                    try:
                        amount, product = self.content[0]
                        self.level -= amount
                    except:
                        pass
                    self.drying_time = self.time_per_liter*amount
                    self.drying_liters = amount
                    if amount > 0:
                        self.cicles += 1
                # Aguarda o tempo de secagem (N [segundos/Litro] * L [Litros])
                time.sleep(self.time_per_liter*amount*TIME_MULTIPLIER)
                if amount > 0:
                    with self.tanklock: self.content.pop(0)
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount*(1-self.loss)/len(self.output_pipes), product)
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, product))
                        self.level += throwback

    def __str__(self):
        with self.tanklock:
            products = {}
            for qtt, product in self.content:
                try: products[product] += qtt
                except: products[product] = qtt
            products = "{:<17}".format(' e '.join(["{:.2f} ({})".format(amount, product_name).ljust(5, ' ') for product_name, amount in products.items()]))
            drying_string = " | {:.2f} L ({:.2f} segs)".format(self.drying_liters, self.drying_time)
            status_string = "{:<30} | {:>10.2f} | ".format(self.name, self.level)
            status_string += products + drying_string
        return status_string