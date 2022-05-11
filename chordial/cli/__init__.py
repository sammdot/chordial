from click_default_group import DefaultGroup

from chordial.cli.admin import admin
from chordial.cli.database import db
from chordial.cli.routes import list_routes
from chordial.cli.start import start

cli = DefaultGroup(default="start", default_if_no_args=True)
cli.add_command(start)
cli.add_command(admin)
cli.add_command(db)
cli.add_command(list_routes)
