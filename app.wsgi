#!/usr/bin/python

# Para correr en apache con wsgi
#
# Incluir en la config:
#
#   Alias /static /var/www/rypto.baicom.com/web/crypto/static
#   WSGIScriptAlias / /var/www/crypto.baicom.com/web/crypto/app.wsgi
 
PROJECT_DIR = '/var/www/crypto.baicom.com/web/crypto'

activate_this = PROJECT_DIR + '/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys, logging

logging.basicConfig(stream=sys.stderr)
sys.path.append(PROJECT_DIR)

from app import app as application
