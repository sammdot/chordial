from http import HTTPStatus
from flask import redirect
from flask_restful import abort, Resource, url_for

from chordial.models import Theory
from chordial.utils.params import fields, params

class TheoryResource(Resource):
  def get(self, theory_id):
    if t := Theory.with_id(theory_id):
      return Theory.schema.dump(t)
    abort(HTTPStatus.NOT_FOUND)

class TheoriesResource(Resource):
  @params(name=fields.Str())
  def get(self, name):
    if name:
      if t := Theory.with_short_name(name):
        return redirect(url_for("theory", theory_id=t.id))
      abort(HTTPStatus.NOT_FOUND)
    return [Theory.schema.dump(t) for t in Theory.all()]
