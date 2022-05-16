from flask import redirect
from flask_restful import abort, Resource
from http import HTTPStatus

from chordial.models import Entry, Translation

class TranslationResource(Resource):
  def get(self, translation_id):
    if tl := Translation.with_id(translation_id):
      entries = Entry.query.filter_by(translation=tl).all()

      return {
        "translation": Translation.full_schema.dump(tl),
        "entries": [Entry.list_schema.dump(e) for e in entries],
      }

    abort(HTTPStatus.NOT_FOUND)
