from click import argument, group, File, option, pass_obj
import logging
import sqlalchemy
import sys

from chordial.models import Base
from chordial.utils.console import print_table
from chordial.utils.database import connect
from chordial.utils.logging import ChordialLogger

@group("db")
@option("--verbose/--no-verbose", "-v")
@pass_obj
def db(ctx, verbose):
  ctx.engine, _ = connect(ctx.config.DATABASE_URL)
  if verbose:
    ChordialLogger.config(
      logging.getLogger("sqlalchemy.engine"), logging.INFO, True, None)

@db.command("create")
@pass_obj
def create_db(ctx):
  Base.metadata.create_all(ctx.engine)

@db.command("query")
@option("--file", "-f", type=File("r"), default=sys.stdin)
@argument("query", type=str, required=False)
@pass_obj
def query_db(ctx, file, query=None):
  if query is None:
    query = sqlalchemy.text(file.read())
  with ctx.engine.connect() as conn:
    cur = conn.execute(query)
    if cur.returns_rows:
      rows = cur.all()
      if rows:
        print_table(rows[0]._fields, rows)
        print(f"{len(rows)} row{'' if len(rows) == 1 else 's'} returned.")
      else:
        print("0 rows returned.")
    else:
      rows = cur.rowcount
      print(f"{rows} row{'' if rows == 1 else 's'} affected.")

@db.command("drop")
@pass_obj
def drop_db(ctx):
  Base.metadata.drop_all(ctx.engine)
