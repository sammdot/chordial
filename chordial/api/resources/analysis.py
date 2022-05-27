from flask_restful import abort, Resource
from http import HTTPStatus

from chordial.models import Outline, Translation


class AnalysisResource(Resource):
  def get(self):
    abort(HTTPStatus.NOT_IMPLEMENTED, message="Analysis function coming soon")
