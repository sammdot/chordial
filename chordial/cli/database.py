from click import group, File, option, pass_obj
import logging
import sqlalchemy
import sys

from chordial.models import Base
from chordial.utils.database import connect
from chordial.utils.logging import ChordialLogger

@group("db")
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
