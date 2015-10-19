from flask import Flask, render_template, request, redirect, jsonify, url_for
from redis import Redis
import string
import random

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

r = Redis(host=app.config['REDIS_HOST'],password=app.config['REDIS_PASSWORD'])
char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
char_len = 10

@app.route('/')
@app.route('/<id>')
def index(id=None):
    js_code = ""
    info = ""

    if id:
        js_code = """
$("#c1").removeClass('active');
$("#m1").removeClass('disabled');
$("#m1").addClass('active');
$("#m2").attr('data-toggle','pill');
$("#tab1").removeClass('in active');
$("#tab3").addClass('in active');
"""
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

        js_code += '$("#msg3").val("%s")' % m

    return render_template('index.html',js_code=js_code,info=info)

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

def randstr():
    return ''.join(random.sample(char_set*char_len,char_len))

if __name__ == '__main__':
    app.run(debug = True)

