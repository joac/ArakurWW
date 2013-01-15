from flask import Flask, url_for, render_template
from flask.ext.bootstrap import Bootstrap
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)

app.config.from_object(__name__)

Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
