from http import HTTPStatus
from flask import redirect
from flask_restful import abort, Resource, url_for

from chordial.api.auth import admin_required
from chordial.models import Layout
from chordial.utils.params import fields, json_params, params

class LayoutResource(Resource):
  def get(self, layout_id):
    if l := Layout.with_id(layout_id):
      return Layout.schema.dump(l)
    abort(HTTPStatus.NOT_FOUND, message=f"No layout with ID {layout_id}")

class LayoutsResource(Resource):
  @params(name=fields.Str())
  def get(self, name=None):
    if name:
      if l := Layout.with_short_name(name):
        return redirect(url_for("layout", layout_id=l.id))
      abort(HTTPStatus.NOT_FOUND, message=f"No layout with ID {layout_id}")
    return [Layout.schema.dump(l) for l in Layout.all()]

  @admin_required
  @json_params(
    short_name=fields.Str(required=True),
    display_name=fields.Str(required=True),
  )
  def post(self, short_name, display_name):
    if l := Layout.with_short_name(short_name):
      abort(HTTPStatus.BAD_REQUEST, message=f"Layout {short_name} already exists")
    if l := Layout.query.filter_by(display_name=display_name).first():
      abort(HTTPStatus.BAD_REQUEST, message=f"Layout {display_name} already exists")

    l = Layout(
      short_name=short_name,
      display_name=display_name,
    )
    l.save()
    return Layout.schema.dump(l)
