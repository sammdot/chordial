from datetime import datetime, timedelta, timezone
from flask import g
from flask_jwt_extended import (
  create_access_token,
  get_jwt,
  get_jwt_identity,
  jwt_required,
  JWTManager,
  set_access_cookies,
  unset_jwt_cookies,
  verify_jwt_in_request,
)

from chordial.models import User
from chordial.utils.uid import encode

jwt = JWTManager()

def setup_auth(app):
  @app.before_request
  def populate_user():
    g.id, g.uid, g.user, g.is_admin = None, None, None, False
    tok = verify_jwt_in_request(optional=True)
    if tok:
      header, data = tok
      g.id = data["sub"]
      g.uid = encode(g.id)
      g.user = User.with_id(g.id)
      g.is_admin = data["is_admin"]

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

def token_for(user, claims=None):
  return create_access_token(identity=user.id, additional_claims=claims)

def get_user_id():
  return get_jwt_identity()

login_required = jwt_required()
login_optional = jwt_required(optional=True)
set_cookies = set_access_cookies
unset_cookies = unset_jwt_cookies
