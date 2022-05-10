from http import HTTPStatus
from flask import g, redirect
from flask_restful import abort, Resource, url_for

from chordial.api.auth import get_user_id, login_optional
from chordial.models import Dictionary, User, Visibility
from chordial.utils.params import fields, params

class DictionaryResource(Resource):
  @login_optional
  def get(self, dict_id):
    if d := Dictionary.with_id(dict_id):
      if (g.id != d.user_id
          and d.visibility == Visibility.private
          and not g.is_admin):
        abort(HTTPStatus.NOT_FOUND)
      if d.proprietary and not g.is_admin:
        return Dictionary.schema.dump(d)
      else:
        return Dictionary.full_schema.dump(d)
    abort(HTTPStatus.NOT_FOUND)

class DictionariesResource(Resource):
  @params(username=fields.Str(required=True), name=fields.Str(required=True))
  def get(self, username, name):
    if d := Dictionary.with_name(username, name):
      return redirect(url_for("dict", dict_id=d.id))
    abort(HTTPStatus.NOT_FOUND)
