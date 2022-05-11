from datetime import datetime
from pytz import UTC

def now():
  return datetime.now(tz=UTC)
