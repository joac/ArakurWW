import time
import random
import math

from flask import Flask, url_for, render_template, Response, json
from flask.ext.bootstrap import Bootstrap
DEBUG = True
SECRET_KEY = 'development key'
BOOTSTRAP_JQUERY_VERSION = None
app = Flask(__name__)

app.config.from_object(__name__)

Bootstrap(app)


def generar_onda( componentes):
    n = 1
    while True:
        total = 0
        for index, value in enumerate(componentes):
            if index % 2:
                total += math.sin(n * value)
            else:
                total += math.cos(n * value)
        yield int(50 + 50 * (total / len(componentes)))
        n += 0.1
        n %= 6

def event_stream():
    oxigeno = generar_onda([0.5, -0.25, 0.125])
    turbiedad = generar_onda([0.5, 0.33, -0.66])
    nivel = generar_onda([1, -0.5])

    while True:
        a = {'oxigen':oxigeno.next(), 'cloudiness': turbiedad.next(), 'level': nivel.next()}
        yield 'data: %s\n\n' % json.dumps(a)
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graficos')
def graficos():
    return render_template('graficos.html')

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0')
