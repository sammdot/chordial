import os

from chordial.config import config_for
from chordial.cli import cli

class Context:
  config = config_for(os.environ.get("CHORDIAL_ENV"))

if __name__ == "__main__":
  cli(prog_name=Context.config.PROGRAM_NAME, obj=Context)
