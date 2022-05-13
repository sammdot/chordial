from enum import Enum
from sqlalchemy.orm import joinedload

from chordial.models.dictionary import Dictionary
from chordial.models.entry import Entry
from chordial.models.outline import Outline
from chordial.models.translation import Translation

class ConflictResolution(Enum):
  overwrite = "overwrite"
  ignore = "ignore"
  restrict = "restrict"

def noop(*args):
  pass

class ImportCallbacks:
  def __init__(self,
    on_init_read=noop,
    on_read_dict=noop,
    on_init_delete=noop,
    on_delete_entry=noop,
    on_init_add_outline=noop,
    on_add_outline=noop,
    on_init_add_translation=noop,
    on_add_translation=noop,
    on_init_add_entry=noop,
    on_add_entry=noop,
    on_begin_commit=noop,
    on_end_commit=noop,
  ):
    self.on_init_read = on_init_read
    self.on_read_dict = on_read_dict
    self.on_init_delete = on_init_delete
    self.on_delete_entry = on_delete_entry
    self.on_init_add_outline = on_init_add_outline
    self.on_add_outline = on_add_outline
    self.on_init_add_translation = on_init_add_translation
    self.on_add_translation = on_add_translation
    self.on_init_add_entry = on_init_add_entry
    self.on_add_entry = on_add_entry
    self.on_begin_commit = on_begin_commit
    self.on_end_commit = on_end_commit

def import_steno_dictionary(
  json: dict, dic: Dictionary, session,
  callbacks=ImportCallbacks(),
  on_conflict=ConflictResolution.overwrite,
):
  l = dic.layout

  outlines = json.keys()
  translations = json.values()

  entries_in_db = {
    o.steno: e for e, o in
    session.query(Entry, Outline).join(Entry.outline)
      .filter(Entry.dictionary == dic).filter(Outline.steno.in_(outlines)).all()
  }
  outlines_in_db = {
    o.steno: o for o in
    session.query(Outline).filter_by(layout=l)
      .filter(Outline.steno.in_(outlines)).all()
  }
  translations_in_db = {
    t.translation: t for t in
    session.query(Translation).filter_by(layout=l)
      .filter(Translation.translation.in_(translations)).all()
  }

  entries_to_add = set()
  entries_to_delete = set()
  outlines = {}
  outlines_to_add = set()
  translations = {}
  translations_to_add = set()

  callbacks.on_init_read(len(entries_in_db))
  for steno, text in json.items():
    callbacks.on_read_dict((steno, text))

    ol = None
    if steno in outlines:
      ol = outlines[steno]
    elif steno in outlines_in_db:
      ol = outlines[steno] = outlines_in_db[steno]
    else:
      ol = outlines[steno] = Outline(steno=steno, layout=l)
      outlines_to_add.add(ol)

    tl = None
    if text in translations:
      tl = translations[text]
    elif text in translations_in_db:
      tl = translations[text] = translations_in_db[text]
    else:
      tl = translations[text] = Translation(translation=text, layout=l)
      translations_to_add.add(tl)

    if steno in entries_in_db:
      e = entries_in_db[steno]
      if e.translation != tl:
        if on_conflict == ConflictResolution.overwrite:
          entries_to_delete.add(e)
        elif on_conflict == ConflictResolution.restrict:
          raise ValueError(f"Entry {e} produces a conflict")
    else:
      e = Entry(outline=ol, translation=tl, dictionary=dic)
      entries_to_add.add(e)

  if outlines_to_add:
    callbacks.on_init_add_outline(len(outlines_to_add))
    for ol in outlines_to_add:
      callbacks.on_add_outline(ol)
      session.add(ol)
    callbacks.on_begin_commit("outlines")
    session.commit()
    callbacks.on_end_commit(len(outlines_to_add))

  if translations_to_add:
    callbacks.on_init_add_translation(len(translations_to_add))
    for tl in translations_to_add:
      callbacks.on_add_translation(tl)
      session.add(tl)
    callbacks.on_begin_commit("translations")
    session.commit()
    callbacks.on_end_commit(len(translations_to_add))

  if entries_to_delete:
    callbacks.on_init_delete(len(entries_to_delete))
    for e in entries_to_delete:
      callbacks.on_delete_entry(e)
      session.delete(e)
    callbacks.on_begin_commit("deleted entries")
    session.commit()
    callbacks.on_end_commit(len(entries_to_delete))

  if entries_to_add:
    callbacks.on_init_add_entry(len(entries_to_add))
    for e in entries_to_add:
      callbacks.on_add_entry(e)
      session.add(e)
    callbacks.on_begin_commit("entries")
    session.commit()
    callbacks.on_end_commit(len(entries_to_add))
