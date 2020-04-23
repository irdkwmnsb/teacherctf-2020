from flask import Flask
import secrets
import os

app = Flask(__name__)


if app.debug:
    secret_path = ".secret"
    app.config['TEMPLATES_AUTO_RELOAD'] = True
else:
    secret_path = "/var/subway/.secret"

if not os.path.exists(secret_path):
    open(secret_path, "wb").write(secrets.token_bytes(32))
app.config["SECRET_KEY"] = open(secret_path, "rb").read()
app.config["TASKS_N"] = 80

import layout.views
