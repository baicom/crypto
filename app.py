from flask import Flask, render_template, request, redirect, jsonify, url_for
from redis import Redis
import string
import random

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
r = Redis(host=app.config['REDIS_HOST'], password=app.config['REDIS_PASSWORD'])

#
# Mostramos el index.html
#


@app.route('/')
@app.route('/<id>')
def index(id=None):
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
