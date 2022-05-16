import threading


class Manager:
    def __init__(self, name, *output_list):
        self.name = name
        self.output_list = list(output_list)
        self.pipe_full = False
        self.pipelock = threading.Lock()

    def __call__(self, valor, product):
        if product == None:
            return valor
        with self.pipelock:
            throwback = 0
            # Verifica se o pipe nao esta cheio
            if not self.pipe_full:
                # Divide a entrada pra cada cada saida
                for output in self.output_list:
                    throwback += output(valor/len(self.output_list), product)
        return throwback