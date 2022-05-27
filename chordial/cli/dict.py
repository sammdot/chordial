from click import argument, Choice, File, group, option, pass_obj
import json
import logging
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
import sys

from chordial.models import Dictionary, import_steno_dictionary
from chordial.models.dict_import import ConflictResolution, ImportCallbacks
from chordial.utils.console import click_callback, print_table, ProgressBar
from chordial.utils.database import connect
from chordial.utils.logging import ChordialLogger
from chordial.utils.uid import decode


@group("dict")
@option("--verbose/--no-verbose", "-v")
@pass_obj
def dict(ctx, verbose):
  _, ctx.session = connect(ctx.config.DATABASE_URL)
  if verbose:
    ctx.verbose = True
    ChordialLogger.config(
      logging.getLogger("sqlalchemy.engine"), logging.INFO, True, None
    )


@dict.command("import")
@option("--file", "-f", type=File("r"), default=sys.stdin)
@option(
  "--on-conflict",
  "-c",
  type=Choice(m.value for m in ConflictResolution),
  default=None,
)
@argument("id", callback=click_callback(decode))
@pass_obj
def dict_import(ctx, file, id, on_conflict):
  try:
    dic = json.load(file)
  except Exception as e:
    print(f"Invalid JSON", file=sys.stderr)
    return

  num_entries = len(dic)

  if d := ctx.session.query(Dictionary).filter_by(id=id).first():
    try:
      with ProgressBar() as p:
        collect = p.add_task(
          "[cyan]Reading existing database", start=False, total=None
        )
        read, delete, add_ol, add_tl, add_e, commit = (
          None,
          None,
          None,
          None,
          None,
          None,
        )

        def read_callback(num):
          nonlocal collect, read
          p.start_task(collect)
          p.update(collect, total=num, completed=num)
          # nonlocal read
          read = p.add_task("[cyan]Reading dictionary", total=num_entries)

        def delete_callback(num):
          nonlocal delete
          delete = p.add_task("[red]Deleting existing entries", total=num)

        def add_outline_callback(num):
          nonlocal add_ol
          add_ol = p.add_task("[green]Adding new outlines", total=num)

        def add_translation_callback(num):
          nonlocal add_tl
          add_tl = p.add_task("[green]Adding new translations", total=num)

        def add_entry_callback(num):
          nonlocal add_e
          add_e = p.add_task("[green]Adding new entries", total=num)

        def begin_commit_callback(item):
          nonlocal commit
          commit = p.add_task(
            f"[blue]Committing {item}", start=False, total=None
          )

        def end_commit_callback(num):
          nonlocal commit
          p.start_task(commit)
          p.update(commit, total=num, completed=num)
          commit = None

        import_steno_dictionary(
          dic,
          d,
          ctx.session,
          callbacks=ImportCallbacks(
            on_init_read=read_callback,
            on_read_dict=lambda _: p.advance(read),
            on_init_delete=delete_callback,
            on_delete_entry=lambda _: p.advance(delete),
            on_init_add_outline=add_outline_callback,
            on_add_outline=lambda _: p.advance(add_ol),
            on_init_add_translation=add_translation_callback,
            on_add_translation=lambda _: p.advance(add_tl),
            on_init_add_entry=add_entry_callback,
            on_add_entry=lambda _: p.advance(add_e),
            on_begin_commit=begin_commit_callback,
            on_end_commit=end_commit_callback,
          ),
          on_conflict=on_conflict,
        )
    except Exception as e:
      import traceback

      traceback.print_exc()
      print(f"Dictionary import failed: {e}", file=sys.stderr)
    return

  print(f"Dictionary {id} does not exist", file=sys.stderr)


@dict.command("ls")
@pass_obj
def dict_list(ctx):
  dicts = ctx.session.query(Dictionary).all()
  columns = ["id", "name", "entries"]
  rows = [(d.id, d.short_name, len(d.entries)) for d in dicts]
  print_table(columns, rows)


@dict.command("clear")
@argument("id", callback=click_callback(decode))
@pass_obj
def dict_clear(ctx, id):
  if d := ctx.session.query(Dictionary).filter_by(id=id).first():
    with ProgressBar() as p:
      read = p.add_task("[red]Deleting entries", total=len(d.entries))
      for entry in d.entries:
        p.update(read, advance=1)
        ctx.session.delete(entry)
      commit = p.add_task("[blue]Committing", start=False, total=None)
      ctx.session.commit()
    return

  print(f"Dictionary {id} does not exist", file=sys.stderr)
