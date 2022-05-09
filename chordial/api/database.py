from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from chordial.models import Base
from chordial.utils.database import connect

def setup_database(app):
  app.engine, app.session = connect(app.config["DATABASE_URL"])
  Base.query = app.session.query_property()
  Base.create_all = lambda: Base.metadata.create_all(app.engine)
