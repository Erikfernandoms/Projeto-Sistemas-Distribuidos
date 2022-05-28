from .tanque import Tank
from env import DEBUG, TIME_MULTIPLIER
import time

class WashTank(Tank):
    def __init__(self, capacity, name, loss, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss
        self.amount = 0
    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            if len(self.output_pipes) > 0:
                # Puxa o proximo da fila
                amount = 0.0
                product = None
                with self.tanklock:
                    try:
                        amount, product = self.content.pop(0)
                        self.level -= amount
                        amount *= (1-self.loss)
                        self.amount = amount
                    except:
                        pass
                    if amount > 0:
                        self.cicles += 1
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount/len(self.output_pipes), 'Biodisel')
                    self.throwback = throwback
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, 'Biodisel'))
                        self.level += throwback

    def __str__(self):
        with self.tanklock:
            products = {}
            for qtt, product in self.content:
                try: products[product] += qtt
                except: products[product] = qtt
            products = ' e '.join(["{:.2f} ({})".format(amount, product_name).ljust(5, ' ') for product_name, amount in products.items()])
            status_string = "{:<30} | {:>10.2f} | {:>10.2f} | {:<6} | ".format(self.name, self.level, self.amount, self.cicles)
            status_string += products
        return status_string