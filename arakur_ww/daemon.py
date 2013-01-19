import time
import json
import redis
import utils
from config import PLC, REDIS
from plc_interface import ArakurPLC
import threading

plc = ArakurPLC(PLC['host'], port=PLC['port'])
plc.connect()

broker = redis.StrictRedis(**REDIS)

class DataAdquisitor(threading.Thread):
    def run(self):
        while True:
            #TODO logica para tratar de que el tiempo del ciclo sea constante
            #TODO guardar en la DB registros historicos
            #TODO agregar logging

            state = plc.obtener_estado()
            broker.publish('plc_state', json.dumps(state))
            time.sleep(1)

class CommandWatcher(threading.Thread):
    def run(self):
        #TODO implementar logging
        pubsub = broker.pubsub()
        pubsub.subscribe('commands')
        for message in pubsub.listen():
            if message['type'] == 'message':
                print message['data']
                utils.execute_command(plc, message['data'])

if __name__ == '__main__':
    da = DataAdquisitor()
    da.daemon = True
    da.start()
    cw = CommandWatcher()
    cw.daemon = True
    cw.start()

    while threading.active_count() > 0:
        time.sleep(0.1)
