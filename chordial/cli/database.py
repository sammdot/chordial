from click import group, File, option, pass_obj
import logging
import sqlalchemy
import sys

from chordial.models import Base
from chordial.utils.console import print_table
from chordial.utils.database import connect
from chordial.utils.logging import ChordialLogger

@group("db")
@option("--quiet/--no-quiet", "-q")
@pass_obj
def db(ctx, quiet):
  ctx.engine, _ = connect(ctx.config.DATABASE_URL)
  if not quiet:
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
  with ctx.engine.connect() as conn:
    rows = conn.execute(query).all()
    if rows:
      print_table(rows[0]._fields, rows)
    else:
      print("No rows.")

@db.command("drop")
@pass_obj
def drop_db(ctx):
  Base.metadata.drop_all(ctx.engine)
