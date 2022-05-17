from env import DEBUG, TIME_MULTIPLIER
import time
import threading

class Tank:
    def __init__(self, capacity, name, stop_signal):
        self.name = name
        self.stop_signal = stop_signal
        self.capacity = capacity
        self.level = 0
        self.content = []
        self.tanklock = threading.Lock()
        self.output_pipes = []
        self.cicles = 0
        # inicia thread do tanque

    def connect_pipe(self, pipe):
        self.output_pipes.append(pipe)

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
                    except:
                        pass
                    if amount > 0:
                        self.cicles += 1
                # Joga para o pipe
                throwback = 0
                for pipe in self.output_pipes:
                    throwback += pipe(amount/len(self.output_pipes), product)
                # Devolve o que restou pro tanque
                if throwback > 0:
                    with self.tanklock:
                        self.content.insert(0, (throwback, product))
                        self.level += throwback

    def start(self):
        thread = threading.Thread(target=self.pump, name="Tank_{}".format(self.name))
        thread.start()
        return thread

    def __call__(self, qtt, product):
        with self.tanklock:
            # Calcula quanto entra no tanque (entry) e quanto volta pelo pile (throwback)
            entry = self.capacity-self.level if qtt + self.level > self.capacity else qtt
            throwback = qtt - entry
            # Adiciona no tanque
            self.level += entry
            if entry > 0:
                self.content.append((entry, product))
        # Devolve pro pipe o que nao coube
        return throwback

    def __str__(self):
        with self.tanklock:
            products = {}
            for qtt, product in self.content:
                try: products[product] += qtt
                except: products[product] = qtt
            products = ' e '.join(["{:.2f} ({})".format(amount, product_name).ljust(5, ' ') for product_name, amount in products.items()])
            status_string = "{:<30} | {:>10.2f} | {:<6} | ".format(self.name, self.level, self.cicles)
            status_string += products
        return status_string
