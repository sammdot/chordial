from click import command, Choice, option, pass_obj
import gunicorn
from gunicorn.app.base import BaseApplication
import logging
from multiprocessing import cpu_count

from chordial import app
from chordial.utils.logging import log, ChordialGunicornLogger


class ChordialApp(BaseApplication):
  def __init__(self, options=None):
    self.options = options or {}
    super().__init__()

  def load_config(self):
    config = {
      k: v
      for k, v in self.options.items()
      if k in self.cfg.settings and v is not None
    }
    for k, v in config.items():
      self.cfg.set(k.lower(), v)

  def load(self):
    return app


@command("start")
@option("--port", "-p", type=int, default=3241)
@option("--workers", "-w", type=int, default=cpu_count() * 2 + 1)
@option(
  "--log-level",
  "-l",
  type=Choice(["debug", "info", "warning", "error", "critical"]),
  default=None,
)
@pass_obj
def start(ctx, port, workers, log_level):
  log_level = log_level or ctx.config.LOG_LEVEL.lower()
  log_to_stdout = ctx.config.LOG_TO_STDOUT
  log.setLevel(log_level.upper())

  gunicorn.SERVER = ctx.config.SERVER_HEADER

  options = {
    "bind": f"0.0.0.0:{port}",
    "reload": ctx.config.DEBUG,
    "workers": workers,
    "loglevel": log_level,
    "proc_name": ctx.config.PROGRAM_NAME,
    "accesslog": "-" if log_to_stdout else ctx.config.ACCESS_LOG,
    "errorlog": "-" if log_to_stdout else ctx.config.ERROR_LOG,
    "logger_class": ChordialGunicornLogger,
  }
  ChordialApp(options).run()
