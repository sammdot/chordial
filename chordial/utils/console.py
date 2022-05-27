from datetime import datetime
from functools import wraps
import re
from rich.console import Console
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.table import Table

from chordial.utils.uid import encode

PROGRESS_COLUMNS = [
  TextColumn("[progress.description]{task.description} ", justify="right"),
  BarColumn(),
  TaskProgressColumn(
    " [progress.percentage]{task.completed:>9,} / {task.total:>9,}",
    "",
    justify="right",
  ),
]


def ProgressBar():
  return Progress(*PROGRESS_COLUMNS)


INITIAL_ZEROS = re.compile("^(0+)")


def replace_initial_zeros(uid):
  return INITIAL_ZEROS.sub(lambda m: ("\xb7" * len(m.group())), uid)


def render_for_console(item, column_name):
  if item is None:
    return "[grey78]<null>[/grey78]"
  elif isinstance(item, bool):
    return f"[blue]{str(item).lower()}[/blue]"
  elif isinstance(item, datetime):
    return item.strftime("%b %d %Y %H:%M:%S")
  elif isinstance(item, int):
    if column_name == "id" or column_name.endswith("_id"):
      return f"[magenta]{replace_initial_zeros(encode(item, 10))}[/magenta]"
    return str(item)
  elif isinstance(item, memoryview) and "password" in column_name:
    return "[grey78]<encrypted>[/grey78]"
  return item


def print_table(column_names, rows):
  table = Table()
  for col in column_names:
    table.add_column(col)
  for row in rows:
    table.add_row(
      *(render_for_console(field, col) for field, col in zip(row, column_names))
    )
  console = Console()
  console.print(table)


def click_callback(fn):
  @wraps(fn)
  def wrapper(_, __, s):
    return fn(s)

  return wrapper
