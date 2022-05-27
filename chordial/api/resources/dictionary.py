from http import HTTPStatus
from flask import current_app, g, redirect, request
from flask_restful import abort, Resource, url_for
from marshmallow_enum import EnumField
from sqlalchemy.sql import func

from chordial.api.auth import login_required
from chordial.models import (
  Dictionary,
  DictionaryFormat,
  Entry,
  Layout,
  User,
  Visibility,
)
from chordial.utils.logging import log
from chordial.utils.params import fields, json_params, params


class DictionaryResource(Resource):
  @params(format=EnumField(DictionaryFormat))
  def get(self, dict_id, format=None):
    if d := Dictionary.with_id(dict_id):
      if (
        g.id != d.user_id
        and d.visibility == Visibility.private
        and not g.is_admin
      ):
        abort(HTTPStatus.NOT_FOUND, message=f"No dictionary with ID {dict_id}")
      should_hide_entries = d.proprietary and not g.is_admin
      if format == DictionaryFormat.json:
        if should_hide_entries:
          abort(
            HTTPStatus.FORBIDDEN,
            message="Proprietary dictionaries may not be downloaded",
          )
        else:
          return d.to_json()
      elif format is None:
        count = (
          current_app.session.query(func.count(Entry.id))
          .filter(Entry.dictionary_id == dict_id)
          .scalar()
        )
        return Dictionary.schema.dump(d) | {"num_entries": count}
      else:
        abort(HTTPStatus.BAD_REQUEST, message=f"Unrecognized format {format}")
    abort(HTTPStatus.NOT_FOUND, message=f"No dictionary with ID {dict_id}")

  @login_required
  def post(self, dict_id):
    if d := Dictionary.with_id(dict_id):
      if d.user.is_system:
        if not g.is_admin:
          abort(
            HTTPStatus.FORBIDDEN,
            message=f"Admin permissions required for system dictionaries",
          )
      elif d.user.id != g.id:
        abort(
          HTTPStatus.FORBIDDEN,
          message=f"Not allowed to import dictionaries for other users",
        )

      dic = request.get_json(force=True, silent=True)
      if not dic:
        abort(HTTPStatus.BAD_REQUEST, message=f"Invalid JSON")

      return import_steno_dictionary(dic, d)
    abort(HTTPStatus.NOT_FOUND, message=f"No dictionary with ID {dict_id}")


class DictionariesResource(Resource):
  @params(username=fields.Str(required=True), name=fields.Str(required=True))
  def get(self, username, name):
    if d := Dictionary.with_name(username, name):
      return redirect(url_for("dict", dict_id=d.id))
    abort(
      HTTPStatus.NOT_FOUND,
      message=f"Dictionary {username}/{name} does not exist",
    )

  @login_required
  @json_params(
    username=fields.Str(),
    short_name=fields.Str(required=True),
    display_name=fields.Str(),
    layout=fields.Str(required=True),
    visibility=EnumField(Visibility),
    proprietary=fields.Boolean(),
  )
  def post(
    self,
    short_name,
    layout,
    username=None,
    display_name=None,
    visibility=Visibility.public,
    proprietary=False,
  ):
    if not username:
      username = g.user.username
    if u := User.with_username(username):
      if u.is_system:
        if not g.is_admin:
          abort(
            HTTPStatus.FORBIDDEN,
            message=f"Admin permissions required for system dictionaries",
          )
      elif u.id != g.id:
        abort(
          HTTPStatus.FORBIDDEN,
          message=f"Not allowed to create dictionaries for other users",
        )

      if l := Layout.with_short_name(layout):
        if d := Dictionary.query.filter_by(user=u, name=short_name).first():
          abort(
            HTTPStatus.BAD_REQUEST,
            message=f"Dictionary {username}/{short_name} already exists",
          )
        elif proprietary and not g.is_admin:
          abort(
            HTTPStatus.BAD_REQUEST,
            message=f"Only system dictionaries may be proprietary",
          )

        d = Dictionary(
          name=short_name,
          display_name=display_name,
          user=u,
          layout=l,
          visibility=visibility,
          proprietary=proprietary,
        )
        d.save()
        return Dictionary.schema.dump(d)

      abort(HTTPStatus.NOT_FOUND, message=f"Layout {layout} does not exist")
    abort(HTTPStatus.NOT_FOUND, message=f"User {username} does not exist")
