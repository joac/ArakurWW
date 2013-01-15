import time
import random

from flask import Flask, url_for, render_template, Response, json
from flask.ext.bootstrap import Bootstrap
DEBUG = True
SECRET_KEY = 'development key'
BOOTSTRAP_JQUERY_VERSION = None
app = Flask(__name__)

app.config.from_object(__name__)

Bootstrap(app)

def event_stream():
    while True:
        a = {'oxigen':random.randint(0, 100), 'cloudiness': random.randint(0, 100), 'level': random.randint(0, 100)}
        yield 'data: %s\n\n' % json.dumps(a)
        time.sleep(0.5)

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
    app.run(threaded=True)
