from click import Choice, File, option, pass_obj
from click_default_group import DefaultGroup
import gunicorn
from gunicorn.app.base import BaseApplication
import logging
from multiprocessing import cpu_count
import os
import sqlalchemy
import sys

from chordial import app
from chordial.config import config_for
from chordial.models import Base
from chordial.utils.database import connect
from chordial.utils.logging import log, ChordialLogger, ChordialGunicornLogger

class ChordialApp(BaseApplication):
  def __init__(self, options=None):
    self.options = options or {}
    super().__init__()

  def load_config(self):
    config = {
      k: v for k, v in self.options.items()
      if k in self.cfg.settings and v is not None}
    for k, v in config.items():
      self.cfg.set(k.lower(), v)

  def load(self):
    return app

cli = DefaultGroup(default="start", default_if_no_args=True)

@cli.command("start")
@option("--port", "-p", type=int, default=3241)
@option("--workers", "-w", type=int, default=cpu_count() * 2 + 1)
@option("--log-level", "-l",
  type=Choice(["debug", "info", "warning", "error", "critical"]),
  default=None)
@pass_obj
def start(ctx, port, workers, log_level):
  log_level = log_level or ctx.config.LOG_LEVEL.lower()
  log_to_stdout = ctx.config.LOG_TO_STDOUT
  log.setLevel(log_level.upper())

  gunicorn.SERVER = ctx.config.SERVER_HEADER

  options = {
    "bind": f"0.0.0.0:{port}",
    "workers": workers,
    "loglevel": log_level,
    "proc_name": ctx.config.PROGRAM_NAME,
    "accesslog": "-" if log_to_stdout else ctx.config.ACCESS_LOG,
    "errorlog": "-" if log_to_stdout else ctx.config.ERROR_LOG,
    "logger_class": ChordialGunicornLogger,
  }
  ChordialApp(options).run()

@cli.group("db")
@pass_obj
def db(ctx):
  ctx.engine, _ = connect(ctx.config.DATABASE_URL)
  ChordialLogger.config(
    logging.getLogger("sqlalchemy.engine"), logging.INFO, True, None)

@db.command("create")
@pass_obj
def create_db(ctx):
  Base.metadata.create_all(ctx.engine)

@db.command("query")
@option("--file", "-f", type=File("r"), default=sys.stdin)
@pass_obj
def query_db(ctx, file):
  query = sqlalchemy.text(file.read())
  ctx.engine.execute(query)

@db.command("drop")
@pass_obj
def drop_db(ctx):
  Base.metadata.drop_all(ctx.engine)

@cli.command("routes")
def list_routes():
  for rule in app.url_map.iter_rules():
    print(rule)

class Context:
  config = config_for(os.environ.get("CHORDIAL_ENV"))

if __name__ == "__main__":
  cli(prog_name="chordial", obj=Context)
