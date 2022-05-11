from time import sleep

class Tanque_Oleo():
    def __init__(self, litros):
        self.litros = litros
        self.tanque = 0
        
    def __call__(self):
        self.tanque += 50 + self.litros
        sleep(1)
        if self.tanque > 0.75:
            self.tanque -= 0.75
        return self.tanque
        