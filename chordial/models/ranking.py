from itertools import groupby

from chordial.models.enums import EntryStatus

ENTRY_STATUS_TO_RANK = {
  EntryStatus.mandatory: 3,
  EntryStatus.recommended: 2,
  EntryStatus.preferred: 1,
  EntryStatus.misstroke: -5,
}

def steno(entry):
  return entry.outline.steno

def translation(entry):
  return entry.translation.translation

def score(entries):
  total = 0
  for entry in entries:
    total += (
      (3 if entry.dictionary.theory else 1) +
      ENTRY_STATUS_TO_RANK.get(entry.status, 0))
  return total

def display_name(entry):
  return f"{entry.dictionary.user.username}/{entry.dictionary.name}"

def rank_by_outline(entries):
  grouped_entries = [
    (steno, sorted(lst, key=display_name)) for steno, lst in
    groupby(sorted(entries, key=steno), key=steno)]
  return sorted([
    (score(lst), steno, lst) for steno, lst in grouped_entries
  ], reverse=True)

def rank_by_translation(entries):
  grouped_entries = [
    (tl, sorted(lst, key=display_name)) for tl, lst in
    groupby(sorted(entries, key=translation), key=translation)]
  return sorted([
    (score(lst), tl, lst) for tl, lst in grouped_entries
  ], reverse=True)
