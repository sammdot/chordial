from click import command
import re

from chordial import app
from chordial.utils.console import print_table

METHODS = ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
URL_PARAM_RE = re.compile(r"<(?:[^>:]+)(:[^>]+)>")
CHECK_MARK = "[green]\u2713[/green]"


@command("routes")
def list_routes():
  rules = []
  supported_methods = set()
  for rule in app.url_map.iter_rules():
    supported_methods |= rule.methods
    rules.append((rule.methods, str(rule)))
  supported_methods = [m for m in METHODS if m in supported_methods]

  print_table(
    supported_methods + ["route"],
    [
      (
        *[CHECK_MARK if m in rule_methods else "" for m in supported_methods],
        URL_PARAM_RE.sub(r"[cyan]\1[/cyan]", rule_string),
      )
      for rule_methods, rule_string in sorted(rules, key=lambda x: x[1])
    ],
  )
