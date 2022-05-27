from http import HTTPStatus
from flask import redirect
from flask_restful import abort, Resource, url_for

from chordial.api.auth import admin_required
from chordial.models import Layout, Theory
from chordial.utils.params import fields, json_params, params


class TheoryResource(Resource):
  def get(self, theory_id):
    if t := Theory.with_id(theory_id):
      return Theory.schema.dump(t)
    abort(HTTPStatus.NOT_FOUND, message=f"No theory with ID {theory_id}")


class TheoriesResource(Resource):
  @params(name=fields.Str())
  def get(self, name=None):
    if name:
      if t := Theory.with_short_name(name):
        return redirect(url_for("theory", theory_id=t.id))
      abort(HTTPStatus.NOT_FOUND, message=f"Theory {name} does not exist")
    return [Theory.schema.dump(t) for t in Theory.all()]

  @admin_required
  @json_params(
    short_name=fields.Str(required=True),
    layout=fields.Str(required=True),
    display_name=fields.Str(),
  )
  def post(self, short_name, layout, display_name=None):
    if t := Theory.with_short_name(short_name):
      abort(
        HTTPStatus.BAD_REQUEST, message=f"Theory {short_name} already exists"
      )
    if l := Layout.with_short_name(layout):
      t = Theory(
        short_name=short_name,
        display_name=display_name,
        layout=l,
      )
      t.save()
      return Theory.schema.dump(t)
    else:
      abort(HTTPStatus.NOT_FOUND, message=f"Layout {layout} does not exist")
