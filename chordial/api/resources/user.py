from http import HTTPStatus
from flask import g, redirect
from flask_restful import abort, Resource, url_for

from chordial.api.auth import get_user_id, login_optional
from chordial.models import User
from chordial.utils.params import fields, params

class UserResource(Resource):
  @login_optional
  def get(self, user_id):
    if u := User.with_id(user_id):
      if g.id == user_id or g.is_admin:
        return User.full_schema.dump(u)
      else:
        return User.schema.dump(u)
    abort(HTTPStatus.NOT_FOUND)

class UsersResource(Resource):
  @params(name=fields.Str(required=True))
  def get(self, name):
    if u := User.with_username(name):
      return redirect(url_for("user", user_id=u.id))
    abort(HTTPStatus.NOT_FOUND)
