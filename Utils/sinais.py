import imp


import threading
import signal

# ====== Sinais e handlers de parada
stop_lock = threading.Lock()
stop_variable = False
def stop_signal():
    global stop_variable, stop_lock
    with stop_lock: 
        return stop_variable
def stop_handler(num, stack):
    global stop_variable
    stop_variable = True
signal.signal(signal.SIGINT, stop_handler)