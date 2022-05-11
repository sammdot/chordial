from datetime import datetime, timedelta
from pytz import UTC

def now():
  return datetime.now(tz=UTC)

def minutes_from_now(minutes):
  return lambda: datetime.now(tz=UTC) + timedelta(minutes=minutes)
