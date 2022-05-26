from env import DEBUG, TIME_MULTIPLIER
import threading
import random
import time


class Input:
    def __init__(self, name, min_qtt, max_qtt, min_periodo, max_periodo, stop_signal):
        self.stop_signal = stop_signal
        self.name = name
        self.input_amount = (min_qtt, max_qtt)
        self.periodo = (min_periodo, max_periodo)
        self.output_pipes = []
        self.inputlock = threading.Lock()
        self.total_input = 0
        self.cicles = 0

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

    def pump(self):
        while not self.stop_signal():
            if DEBUG: time.sleep(TIME_MULTIPLIER)
            # Sorteia a quantidade de entrada no range
            amount = random.SystemRandom().uniform(self.input_amount[0], self.input_amount[1])
            with self.inputlock:
                self.total_input += amount
                self.cicles += 1
            # Emite o valor pelos pipes
            for pipe in self.output_pipes:
                pipe(amount/len(self.output_pipes), self.name)
            # espera
            wait_time = random.SystemRandom().uniform(self.periodo[0], self.periodo[1])
            time.sleep(wait_time*TIME_MULTIPLIER)

    def start(self):
        thread = threading.Thread(target=self.pump, name="Input_{}".format(self.name))
        thread.start()
        return thread

    def __str__(self):
        with self.inputlock:
            log = self.name.ljust(20, ' ')
            return "{:<20} | {:<25.2f} | {:<6}".format(self.name, self.total_input, self.cicles)


