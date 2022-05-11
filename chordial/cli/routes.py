from click import command

from chordial import app

@command("routes")
def list_routes():
  for rule in app.url_map.iter_rules():
    print(rule)
