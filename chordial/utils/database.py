from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from chordial.models import Base

def connect(url):
  engine = create_engine(url, connect_args={"check_same_thread": False})
  Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  session = scoped_session(Session)
  return (engine, session)
