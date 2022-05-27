from flask import redirect
from flask_restful import abort, Resource, url_for
from http import HTTPStatus

from chordial.models import Entry, Layout, Outline, Translation
from chordial.models.ranking import rank_by_outline, rank_by_translation
from chordial.utils.params import fields, params


class EntryResource(Resource):
  def get(self, entry_id):
    if e := Entry.with_id(entry_id):
      ol, tl = e.outline, e.translation

      same_outline = Entry.query.filter_by(outline=ol).all()
      same_translation = Entry.query.filter_by(translation=tl).all()

      return {
        "layout": Layout.list_schema.dump(ol.layout),
        "entry": Entry.schema.dump(e),
        "related": {
          "outline": [
            {
              "score": score,
              "translation": translation,
              "entries": [Entry.schema.dump(e) for e in entries],
            }
            for (score, translation, entries) in rank_by_translation(
              same_outline
            )
          ],
          "translation": [
            {
              "score": score,
              "outline": outline,
              "entries": [Entry.schema.dump(e) for e in entries],
            }
            for (score, outline, entries) in rank_by_outline(same_translation)
          ],
        },
      }
    abort(HTTPStatus.NOT_FOUND, message=f"No entry with ID {entry_id}")


class EntryByIdsResource(Resource):
  def get(self, outline_id, translation_id):
    if e := Entry.query.filter_by(
      outline_id=outline_id, translation_id=translation_id
    ).first():
      return redirect(url_for("entry", entry_id=e.id))
    abort(
      HTTPStatus.NOT_FOUND,
      message=f"No entry with outline {outline_id} and translation {translation_id}",
    )


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

      ok = False

      q = Entry.query
      if steno:
        ol = Outline.with_steno(steno, layout=l)
        if not ol:
          abort(HTTPStatus.NOT_FOUND, message=f"Steno '{steno}' not found")
        search_params["outline"] = Outline.schema.dump(ol)
        q = q.filter_by(outline_id=ol.id)
        ok = True
      if translation:
        tl = Translation.with_text(translation, layout=l)
        if not tl:
          abort(
            HTTPStatus.NOT_FOUND,
            message=f"Translation '{translation}' not found",
          )
        search_params["translation"] = Translation.schema.dump(tl)
        q = q.filter_by(translation_id=tl.id)
        ok = True

      if not ok:
        abort(
          HTTPStatus.BAD_REQUEST,
          message="Must specify at least one of steno or translation",
        )

      entries = q.all()
      response = {
        "layout": Layout.list_schema.dump(l),
        "search": search_params,
      }
      if steno and translation:
        response["entries"] = [Entry.schema.dump(e) for e in entries]

      if steno:
        response["entries_ranked"] = [
          {
            "score": score,
            "translation": translation,
            "entries": [Entry.schema.dump(e) for e in entries],
          }
          for (score, translation, entries) in rank_by_translation(entries)
        ]
      elif translation:
        response["entries_ranked"] = [
          {
            "score": score,
            "outline": outline,
            "entries": [Entry.schema.dump(e) for e in entries],
          }
          for (score, outline, entries) in rank_by_outline(entries)
        ]

      return response

    abort(
      HTTPStatus.NOT_FOUND,
      message=f"Steno '{steno}' and translation '{translation}' not found",
    )
