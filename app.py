from flask import Flask, render_template, request, redirect, jsonify, url_for
from redis import Redis
import string
import random

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
r = Redis(host=app.config['REDIS_HOST'],password=app.config['REDIS_PASSWORD'])

#
# Mostramos el index.html
#
@app.route('/')
@app.route('/<id>')
def index(id=None):
    return render_template('index.html')

#
# Manejamos /get via json
# Busca el id en el servidor redis
#
@app.route('/get', methods=['POST'])
def get():
    id = request.form.get('id')
    info = ""

    m = r.get(id)
    if m == None:
        m = "No existe el mensaje"
    else:
        secs = r.ttl(id)
        info = "&nbsp; Expira en %d d&iacute;a/s" % (secs/86400)
        if m.find('destroy') == 0:
            destroy = 1
            m = m.replace('destroy','')
            r.delete(id) 
            info += ", destruir al leer"

    # TODO
    # el tiempo de expiracion y el flag destroy se comunican por texto
    # se deberia informar en el json y el main.js parsearlo 

    return jsonify({'info':info,'msg':m})

#
# Manejamos /post via un formulario
# Guarda el mensaje encriptado en el servidor redis
#
@app.route('/post', methods=['POST'])
def post():
    msg1 = request.form['msg1']
    expire = request.form['expire']
    rand = randstr()

    if 'destroy' in request.form:
        msg1 = 'destroy' + msg1

    p = r.pipeline()
    p.set(rand,msg1)
    p.expire(rand,expire)
    p.execute()

    return request.url_root + rand, 200 

#
# Genera el random string (mayusculas, minusculas y digitos)
#
def randstr():
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    char_len = 10

    return ''.join(random.sample(char_set*char_len,char_len))

if __name__ == '__main__':
    app.run(debug = True)

