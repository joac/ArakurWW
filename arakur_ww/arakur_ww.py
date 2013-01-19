import time
import random
import math
import redis

from flask import Flask, url_for, render_template, Response, json, jsonify
from flask.ext.bootstrap import Bootstrap
import utils

DEBUG = True
SECRET_KEY = 'development key'
BOOTSTRAP_JQUERY_VERSION = None
app = Flask(__name__)

app.config.from_object(__name__)

Bootstrap(app)

broker = redis.StrictRedis(host='localhost', port=6379, db=0)

def enviar_comando(function_name, *args, **kwargs):
    return broker.publish('commands', utils.remote_plc_command(function_name, *args, **kwargs))

def generar_onda( componentes):
    n = 1
    while True:
        total = 0
        for index, value in enumerate(componentes):
            if index % 2:
                total += math.sin(n * value)
            else:
                total += math.cos(n * value)
        yield 50 + (50 * (total / len(componentes)) * math.cos(0.1*n))
        n += 0.1
        n %= 2000

def event_stream():
    stream = broker.pubsub()
    stream.subscribe('plc_state')
    for data in stream.listen():
        if data['type'] == 'message':
            yield 'data: %s\n\n' % data['data']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graficos')
def graficos():
    return render_template('graficos.html')

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/iniciar/<int:programa>')
def iniciar_programa(programa):
    if programa in xrange(1, 5):
        enviar_comando('iniciar_programa', programa)

    return "HEllooo"

@app.route('/actualizar/<int:programa>', methods='POST')
def actualizar_programa(programa):
    return programa

@app.route('/registro/<int:direccion>/<int:valor>/')
def actualizar_registro(direccion, valor):
    enviar_comando('_escribir_registro', direccion, valor)
    return "enviado!"

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
