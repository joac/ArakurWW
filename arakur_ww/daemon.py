import time
import json
import redis
import utils
from utils import RemoteCommand
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
            #guardamos en una key programa_<n> el hash del programa
            #TODO actualizar solo si hay novedades
            for n, programa in enumerate(state['programs'], 1):
                broker.hmset('programa_%s' % n, programa)

            broker.publish('plc_state', json.dumps(state))
            time.sleep(0.5)

class CommandWatcher(threading.Thread):
    def run(self):
        #TODO implementar logging
        pubsub = broker.pubsub()
        pubsub.subscribe('commands')
        for message in pubsub.listen():
            if message['type'] == 'message':
                print message['data']
                command = RemoteCommand()
                command.unserialize(message['data'])
                success = command.execute(plc)
                response = {'id':command.id, 'success': success}
                print response
                time.sleep(0.6)
                broker.publish('command-returns', json.dumps(response))

if __name__ == '__main__':
    da = DataAdquisitor()
    da.daemon = True
    da.start()
    cw = CommandWatcher()
    cw.daemon = True
    cw.start()

    while threading.active_count() > 0:
        time.sleep(0.1)
