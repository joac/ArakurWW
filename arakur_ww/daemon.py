from threading import Thread
import time
import json
import redis
import utils

from plc_interface import ArakurPLC

plc = ArakurPLC('localhost', port=5020)
plc.connect()

broker = redis.StrictRedis(host='localhost', port=6379, db=0)

class DataAdquisitor(Thread):
    def run(self):
        while True:
            #state = {}
            #state['marcas'] = plc.leer_marcas()
            #state['registros'] = plc.leer_registros()
            state = plc.obtener_estado()

            broker.publish('plc_state', json.dumps(state))
            time.sleep(1)

class CommandWatcher(Thread):
    def run(self):
        print "corriendo test"
        pubsub = broker.pubsub()
        pubsub.subscribe('commands')
        print pubsub
        for message in pubsub.listen():
            if message['type'] == 'message':
                print message['data']
                utils.execute_command(plc, message['data'])

if __name__ == '__main__':
    da = DataAdquisitor()
    da.start()
    cw = CommandWatcher()
    cw.start()
