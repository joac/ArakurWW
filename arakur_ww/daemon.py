#! -*-coding: utf8-*-
import time
import json
import redis
import utils
from utils import RemoteCommand
from config import PLC, REDIS
from plc_interface import ArakurPLC
import threading
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


plc = ArakurPLC(PLC['host'], port=PLC['port'])
plc.connect()

broker = redis.StrictRedis(**REDIS)

class DataAdquisitor(threading.Thread):
    def run(self):
        while True:
            #TODO logica para tratar de que el tiempo del ciclo sea constante
            #TODO guardar en la DB registros historicos
            #TODO agregar logging
            try:
                state = plc.obtener_estado()
                logging.info("Obtenidos datos del PLC")
                #guardamos en una key programa_<n> el hash del programa
                for n, programa in enumerate(state['programs'], 1):
                    broker.hmset('programa_%s' % n, programa)

                broker.hmset('params', state['params'])
                broker.publish('plc_state', json.dumps(state))
                logging.info("Estado publicado en canal 'plc_state'")
            except:
                logging.error("Ocurrió un error al obtener los datos desde el PLC")
            time.sleep(0.5)


class CommandWatcher(threading.Thread):
    def run(self):
        #TODO implementar logging
        pubsub = broker.pubsub()
        pubsub.subscribe('commands')
        for message in pubsub.listen():
            if message['type'] == 'message':
                logging.info("Se recibió el mensaje de ejecución remota %s", message['data'])
                command = RemoteCommand()
                command.unserialize(message['data'])
                try:
                    success = command.execute(plc)
                except:
                    success = False
                    logging.error("No se pudo ejecutar la orden: '%s'", command.function_name)

                response = {'id':command.id, 'success': success}
                time.sleep(0.6)
                broker.publish('command-returns', json.dumps(response))
                logging.info("enviada respuesta a comando: '%'", response)

if __name__ == '__main__':
    da = DataAdquisitor()
    da.daemon = True
    da.start()
    cw = CommandWatcher()
    cw.daemon = True
    cw.start()

    while threading.active_count() > 0:
        time.sleep(0.1)
