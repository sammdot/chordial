from flask import redirect
from flask_restful import abort, Resource, url_for
from http import HTTPStatus

from chordial.models import Entry, Layout, Outline, Translation
from chordial.utils.params import fields, params

class EntryResource(Resource):
  def get(self, entry_id):
    if e := Entry.with_id(entry_id):
      ol, tl = e.outline, e.translation

      same_outline = Entry.query.filter_by(outline=ol).all()
      same_translation = Entry.query.filter_by(translation=tl).all()

      return {
        "layout": Layout.schema.dump(ol.layout),
        "entry": Entry.schema.dump(e),
        "related": {
          "outline": [Entry.schema.dump(e) for e in same_outline],
          "translation": [Entry.schema.dump(e) for e in same_translation],
        },
      }
    abort(HTTPStatus.NOT_FOUND)

class EntriesResource(Resource):
  @params(
    layout=fields.Str(required=True),
    steno=fields.Str(),
    translation=fields.Str(),
  )
  def get(self, layout, steno=None, translation=None):
    if l := Layout.with_short_name(layout):
      ol, tl = None, None
      search_params = {}

      q = Entry.query
      if steno:
        ol = Outline.with_steno(steno, layout=l)
        if not ol:
          abort(HTTPStatus.NOT_FOUND, message=f"Steno '{steno}' not found")
        search_params["outline"] = Outline.schema.dump(ol)
        q = q.filter_by(outline_id=ol.id)
      if translation:
        tl = Translation.with_text(translation, layout=l)
        if not tl:
          abort(HTTPStatus.NOT_FOUND,
            message=f"Translation '{translation}' not found")
        search_params["translation"] = Translation.schema.dump(tl)
        q = q.filter_by(translation_id=tl.id)

      entries = q.all()
      return {
        "layout": Layout.schema.dump(l),
        "search": search_params,
        "entries": [Entry.schema.dump(e) for e in entries],
      }

    abort(HTTPStatus.NOT_FOUND)
