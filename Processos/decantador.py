from .tanque import Tank
from env import DEBUG, TIME_MULTIPLIER
import time

class Decanter(Tank):
    # A saida do decantador é 0.02 Glicerina, 0.09 EtOH e 0.89 Solucao p/ lavagem
    def __init__(self, capacity, name, stop_signal):
        super().__init__(capacity, name, stop_signal)
        self.glycerin_pipe = None
        self.etoh_pipe = None
        self.wash_pipe = None

    def connect_glycerin_pipe(self, pipe):
        self.glycerin_pipe = pipe

    def connect_etoh_pipe(self, pipe):
        self.etoh_pipe = pipe
        
    def connect_wash_pipe(self, pipe):
        self.wash_pipe = pipe

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            # remove tudo o que tiver nele
            total = 0
            with self.tanklock:
                total = sum([amount for amount, _ in self.content])
                self.content.clear()
                self.level -= total
                if total > 0:
                    self.cicles += 1
            # Joga para o pipe
            throwback = 0
            throwback += self.glycerin_pipe(0.02*total, 'Glicerina')
            throwback += self.etoh_pipe(0.09*total, 'EtOH')
            throwback += self.wash_pipe(0.89*total, 'Lavagem')
            # Devolve o que restou pro tanque
            if throwback > 0:
                with self.tanklock:
                    self.content.insert(0, (throwback, 'throwback'))
                    self.level += throwback