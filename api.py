from flask import Flask, request, redirect, jsonify, url_for, json
from redis import Redis
from flask_cors import CORS, cross_origin
from flasgger import Swagger
import string
import random

app = Flask(__name__)
cors = CORS(app)
swag = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "description": "Este es la documentación  de como llamar a la app de [BAICOM Crypto](http://crypto.baicom.com).",
            "version": "1.0.0",
            "title": "Baicom Crypto",
        },
        "consumes": ["application/json", ],
        "produces": ["application/json", ],
        "contact": {"email": "info@baicom.com"},
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
        },
        "host": "localhost:5100",
        "basePath": "/",
        "tags": [
            {
                "name": "Crypto",
                "description": "Agrupacíión de llamadas a encriptar mensaje",
            }
        ],
        "schemes": ["http", "https"],
        "definitions": {
            "Msg": {
                "type": "object",
                "properties": {
                    "msg1": {"type": "string", "description": "mensaje ya encriptado"},
                    "expire": {
                        "type": "integer",
                        "format": "int64",
                        "description": "Segundos de vigencia del mensaje",
                        "example": 2592000,
                    },
                    "destroy": {
                        "type": "boolean",
                        "description": "Flag que indica si se destruye el mensaje al leerlo",
                    },
                },
            },
            "MsgReturn": {
                "type": "object",
                "properties": {
                    "info": {
                        "type": "string",
                        "description": "Rertorna en texto el tiempo de expirado o si se destriyo al leerlo",
                    },
                    "msg": {
                        "type": "string",
                        "description": "Mensaje propiamente dicho",
                    },
                    "id": {
                        "type": "integer",
                        "description": "Identificador del mensaje",
                    },
                },
                "xml": {"name": "Msg"},
            },
            "MsgCreated": {
                "type": "object",
                "properties": {
                    "msgid": {
                        "type": "string",
                        "description": "Identidicador con el id que se generó en la base de datos",
                    }
                },
                "xml": {"name": "MsgCreated"},
            },
        },
        "externalDocs": {"description": "about Swagger", "url": "http://swagger.io"},
    },
)

app.config.from_pyfile("app.cfg")
r = Redis(host=app.config["REDIS_HOST"], password=app.config["REDIS_PASSWORD"])


@app.route("/", methods=["GET"])
def empty():
    return jsonify({"error": "Ausencia del parametro ID"}), 400


@app.route("/<id>", methods=["GET"])
@cross_origin()
def index(id=None):
    """
      Retorna el mensaje persistido en la base de datos
      Retorna el mensaje que se le pasa por path, este mensaje se retorna de la base redis de acuerdo como este.
      También retorna si se autodestruyó cuando se leyó
      ----
      tags:
          - "Crypto"
      produces:
        - "application/json"
      parameters:
        - name: "id"
          in: "path"
          description: "Identificador del mensaje"
          required: true
          type: "string"
          default: ""
          example: "zAhwkUlayG"
      responses:
        "200":
          description: "Mensaje creado con exito"
          schema:
            description: "Id de mensaje creado"
            items:
              $ref: "#/definitions/MsgReturn"
        "400":
          description: "Invalid status value"
        "401":
          description: "Not data found"
    """
    info = ""
    code = 200
    m = r.get(id)
    if m == None:
        info = "No existe el mensaje"
        code = 404
        m = ""
    else:
        secs = r.ttl(id)
        info = "Expira en %d dias" % (secs / 86400)
        m = m.decode()
        if m.find("destroy") == 0:
            destroy = 1
            m = m.replace("destroy", "")
            r.delete(id)
            info += ", destruir al leer"
            code = 200

    return jsonify({"info": info, "msg": m, "id": id}), code


@app.route("/", methods=["POST"])
def post():
    """
      Crear un nuevo mensaje encriptado
      ---
      tags:
        - "Crypto"
      consumes:
        - "application/json"
      produces:
        - "application/json"
      parameters:
        - in: "body"
          name: "msg"
          description: "Mensaje ya encriptado"
          required: true
          schema:
            $ref: "#/definitions/Msg"
      responses:
        "201":
          description: "Mensaje creado con exito"
          schema:
            description: "Id de mensaje creado"
            items:
              $ref: "#/definitions/MsgCreated"
        "400":
          description: "Bad request"
        "401":
          description: "No tiene permisos"
    """
    req_data = json.loads(request.data)
    if req_data == None:
        return jsonify({"msgid": "payload empty"}), 400

    msg1 = req_data["msg1"]
    expire = req_data["expire"]
    if "destroy" in req_data:
        destroy = 'destroy'
    else:
        destroy = ''

    rand = randstr()

    msg1 = destroy + msg1

    p = r.pipeline()
    p.set(rand, msg1)
    p.expire(rand, expire)
    p.execute()

    return jsonify({"msgid": rand}), 201


#
# Genera el random string (mayusculas, minusculas y digitos)
#
def randstr():
    char_set = string.ascii_uppercase + string.ascii_lowercase + string.digits
    char_len = 10

    return "".join(random.sample(char_set * char_len, char_len))


if __name__ == "__main__":
    app.run(debug=True, port=5100)
