from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import force_instant_defaults

from chordial.models import Base
from chordial.utils.database import connect


def setup_database(app):
  app.engine, app.session = connect(app.config["DATABASE_URL"])
  Base.query = app.session.query_property()
  Base.create_all = lambda: Base.metadata.create_all(app.engine)
  Base.save = lambda self: [app.session.add(self), app.session.commit()][-1]
  force_instant_defaults()
