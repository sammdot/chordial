from enum import Enum
from flask import current_app, g, redirect
from flask_restful import abort, Resource
from http import HTTPStatus
from marshmallow_enum import EnumField

from chordial.models import (
  Dictionary,
  Entry,
  Outline,
  Translation,
)
from chordial.utils.params import fields, json_params, params

class EntrySorting(Enum):
  steno = Outline.steno
  translation = Translation.translation

class DictionaryEntriesResource(Resource):
  @params(
    offset=fields.Int(),
    count=fields.Int(),
    sort=EnumField(EntrySorting),
  )
  def get(self, dict_id, offset=0, count=100, sort=EntrySorting.steno):
    if d := Dictionary.with_id(dict_id):
      if d.proprietary and not g.is_admin:
        abort(HTTPStatus.FORBIDDEN,
          message="Admin permissions required for proprietary dictionaries")
      entries = (
        current_app.session.query(Entry).join(Outline).join(Translation)
          .filter(Entry.dictionary_id == dict_id).order_by(sort)
          .offset(offset).limit(count).all())
      return {
        "count": count,
        "offset": offset,
        "entries": [Entry.schema.dump(e) for e in entries],
      }
    abort(HTTPStatus.NOT_FOUND, message=f"No dictionary with ID {dict_id}")
