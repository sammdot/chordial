from http import HTTPStatus
from flask import g, make_response, request
from flask_restful import abort, Resource

from chordial.api.auth import login_required, set_cookies, token_for, unset_cookies
from chordial.models import User
from chordial.utils.params import fields, json_params

class AuthResource(Resource):
  @json_params(username=fields.Str(required=True), password=fields.Str(required=True))
  def post(self, username, password):
    if user := User.with_username(username):
      if user.verify_password(password):
        claims = {"is_admin": True} if user.is_admin else None
        token = token_for(user, claims=claims)
        res = make_response({"access_token": token})
        set_cookies(res, token)
        return res
    abort(HTTPStatus.BAD_REQUEST, message="Invalid username or password")

  @login_required
  def get(self):
    if u := User.with_id(g.id):
      return User.auth_schema.dump(u)
    abort(HTTPStatus.NOT_FOUND)

  @login_required
  def delete(self):
    res = make_response({})
    unset_cookies(res)
    return res
