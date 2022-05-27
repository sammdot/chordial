import gunicorn.glogging as glogging
import logging
from logging import (
  currentframe,
  FileHandler,
  Formatter,
  Logger,
  StreamHandler,
)
import os
import sys

LOG_FORMAT = "{levelname:1.1}{asctime} {process}/{threadName} {filename}:{lineno}] {message}"
DATE_FORMAT = "%m%d %H:%M:%S"
ACCESS_FORMAT = (
  "{levelname:1.1}{asctime} {process}/{threadName} access.log:0] {message}"
)

WRONG_CALLERS = [
  os.path.normcase(f)
  for f in [
    logging.__file__,
    glogging.__file__,
    __file__,
  ]
]


def is_wrong_caller(filename):
  return filename in WRONG_CALLERS


# Modified from CPython's implementation, but also takes care of
# Gunicorn's logging layer
def find_caller(stack_info=False, stacklevel=1):
  f = logging.currentframe()
  if f is not None:
    f = f.f_back
  orig_f = f
  while f and stacklevel > 1:
    f = f.f_back
    stacklevel -= 1
  if not f:
    f = orig_f
  rv = "(unknown file)", 0, "(unknown function)", None
  while hasattr(f, "f_code"):
    co = f.f_code
    filename = os.path.normcase(co.co_filename)
    if is_wrong_caller(filename):
      f = f.f_back
      continue
    sinfo = None
    if stack_info:
      sio = io.StringIO()
      sio.write("Stack (most recent call last):\n")
      traceback.print_stack(f, file=sio)
      sinfo = sio.getvalue()
      if sinfo[-1] == "\n":
        sinfo = sinfo[:-1]
      sio.close()
    rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
    break
  return rv


class ChordialGunicornLogger(glogging.Logger):
  def setup(self, cfg):
    super().setup(cfg)
    self._set_handler(
      self.error_log,
      cfg.errorlog,
      fmt=Formatter(LOG_FORMAT, DATE_FORMAT, style="{"),
    )
    if cfg.accesslog:
      self._set_handler(
        self.access_log,
        cfg.accesslog,
        fmt=Formatter(ACCESS_FORMAT, DATE_FORMAT, style="{"),
        stream=sys.stdout,
      )

    self.error_log.findCaller = find_caller
    self.access_log.findCaller = find_caller


class ChordialLogger(Logger):
  def __init__(self):
    super().__init__("chordial")
    self.findCaller = find_caller

  def config(self, log_level, log_to_stdout, log_file):
    self.setLevel(log_level)

    if log_to_stdout:
      handler = StreamHandler()
    else:
      handler = FileHandler(log_file)
    handler.setFormatter(Formatter(LOG_FORMAT, DATE_FORMAT, style="{"))
    self.addHandler(handler)


log = ChordialLogger()
