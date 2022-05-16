from .tanque import Tank
from env import DEBUG, TIME_MULTIPLIER
import time

class WashTank(Tank):
    def __init__(self, capacity, name, loss, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.loss = loss

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
                    except:
                        pass
                    if amount > 0:
                        self.cicles += 1
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount/len(self.output_pipes), 'Biodisel')
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, 'Biodisel'))
                        self.level += throwback