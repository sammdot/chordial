from flask import redirect
from flask_restful import abort, Resource
from http import HTTPStatus

from chordial.models import Entry, Layout, Outline


class OutlineResource(Resource):
  def get(self, outline_id):
    if ol := Outline.with_id(outline_id):
      entries = Entry.query.filter_by(outline=ol).all()

      return {
        "layout": Layout.schema.dump(ol.layout),
        "outline": Outline.full_schema.dump(ol),
        "entries": [Entry.list_schema.dump(e) for e in entries],
      }

    abort(HTTPStatus.NOT_FOUND, message=f"No outline with ID {outline_id}")
