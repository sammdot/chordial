class Config:
  DEBUG = True
  DATABASE_URL = "sqlite:///chordial.db"

  PROCESS_NAME = "chordial"
  LOG = "chordial.log"
  ACCESS_LOG = "chordial.access.log"
  ERROR_LOG = "chordial.error.log"
  LOG_LEVEL = "debug"
  LOG_TO_STDOUT = True

class DevelopmentConfig(Config):
  pass

class StagingConfig(DevelopmentConfig):
  DEBUG = False

  LOG_LEVEL = "info"
  LOG_TO_STDOUT = False

class ProductionConfig(StagingConfig):
  pass

def config_for(env):
  return (
    ProductionConfig if env == "production" else
      StagingConfig if env == "staging" else DevelopmentConfig)()
