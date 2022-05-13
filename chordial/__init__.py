from flask import Flask
from flask_cors import CORS
import os

from chordial.api import api
from chordial.api.database import setup_database
from chordial.api.auth import jwt, setup_auth
from chordial.config import config_for
from chordial.utils.uid import uid_converter

def create_app(env):
  app = Flask(__name__)
  app.config.from_object(config_for(env))

  for length in [4, 6, 8, 10]:
    app.url_map.converters[f"uid{length}"] = uid_converter(length)

  api.init_app(app)
  CORS(app)
  setup_database(app)
  jwt.init_app(app)
  setup_auth(app)

  return app

app = create_app(os.environ.get("CHORDIAL_ENV"))
