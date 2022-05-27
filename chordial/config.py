from datetime import timedelta


class Config:
  DEBUG = True
  DATABASE_URL = "sqlite:///chordial.db"

  PROGRAM_NAME = "chordial"
  VERSION = "devel"

  LOG = "chordial.log"
  ACCESS_LOG = "chordial.access.log"
  ERROR_LOG = "chordial.error.log"
  LOG_LEVEL = "debug"
  LOG_TO_STDOUT = True

  SERVER_HEADER = f"{PROGRAM_NAME}/{VERSION}"

  JWT_COOKIE_SECURE = False
  JWT_ACCESS_COOKIE_NAME = "access_token"
  JWT_REFRESH_COOKIE_NAME = "refresh_token"
  JWT_TOKEN_LOCATION = ["cookies", "headers"]
  JWT_SECRET_KEY = "CHANGE_THIS"
  JWT_SESSION_COOKIE = False
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class DevelopmentConfig(Config):
  pass


class StagingConfig(DevelopmentConfig):
  DEBUG = False
  DATABASE_URL = "CHANGE_THIS"

  LOG_LEVEL = "info"
  LOG_TO_STDOUT = False

  JWT_COOKIE_SECURE = True
  JWT_SECRET_KEY = "CHANGE_THIS"


class ProductionConfig(StagingConfig):
  DATABASE_URL = "CHANGE_THIS"

  JWT_SECRET_KEY = "CHANGE_THIS"


def config_for(env):
  return (
    ProductionConfig
    if env == "production"
    else StagingConfig
    if env == "staging"
    else DevelopmentConfig
  )()
