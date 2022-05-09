from datetime import datetime, timedelta, timezone
from flask_jwt_extended import (
  create_access_token,
  get_jwt,
  get_jwt_identity,
  jwt_required,
  JWTManager,
  set_access_cookies,
  unset_jwt_cookies,
)

jwt = JWTManager()

def setup_auth(app):
  @app.after_request
  def refresh_expiring_jwts(response):
    try:
      exp_timestamp = get_jwt()["exp"]
      now = datetime.now(timezone.utc)
      target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
      if target_timestamp > exp_timestamp:
        access_token = create_access_token(identity=get_jwt_identity())
        set_access_cookies(response, access_token)
      return response
    except (RuntimeError, KeyError):
      return response

def token_for(user):
  return create_access_token(identity=user.username)

def get_user():
  return get_jwt_identity()

login_required = jwt_required()
set_cookies = set_access_cookies
unset_cookies = unset_jwt_cookies
