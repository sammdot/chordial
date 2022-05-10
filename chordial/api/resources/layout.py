from http import HTTPStatus
from flask import redirect
from flask_restful import abort, Resource, url_for

from chordial.models import Layout
from chordial.utils.params import fields, params

class LayoutResource(Resource):
  def get(self, layout_id):
    if l := Layout.with_id(layout_id):
      return Layout.schema.dump(l)
    abort(HTTPStatus.NOT_FOUND)

class LayoutsResource(Resource):
  @params(name=fields.Str())
  def get(self, name=None):
    if name:
      if l := Layout.with_short_name(name):
        return redirect(url_for("layout", layout_id=l.id))
      abort(HTTPStatus.NOT_FOUND)
    return [Layout.schema.dump(l) for l in Layout.all()]
