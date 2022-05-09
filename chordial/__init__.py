from flask import Flask
import os

from chordial.config import config_for

def create_app(env):
  app = Flask(__name__)
  app.config.from_object(config_for(env))

  return app

app = create_app(os.environ.get("CHORDIAL_ENV"))
