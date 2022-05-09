from flask import Flask
import os

from chordial.api import api
from chordial.api.database import setup_database
from chordial.api.auth import jwt, setup_auth
from chordial.config import config_for

def create_app(env):
  app = Flask(__name__)
  app.config.from_object(config_for(env))

  api.init_app(app)
  setup_database(app)
  jwt.init_app(app)
  setup_auth(app)

  return app

app = create_app(os.environ.get("CHORDIAL_ENV"))
