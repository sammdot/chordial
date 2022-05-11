from click import argument, group, pass_obj
import sys

from chordial.models import User
from chordial.utils.database import connect

@group("admin")
@pass_obj
def admin(ctx):
  ctx.engine, _ = connect(ctx.config.DATABASE_URL)

@admin.command("ls")
@pass_obj
def list_admins(ctx):
  admins = User.query.filter_by(is_admin=True).all()
  for admin in admins:
    print(admin)
  else:
    print(f"No admins.")

@admin.command("grant")
@argument("user", type=str)
@pass_obj
def grant_admin(ctx, user):
  if user := User.query.filter_by(username=user).first():
    if user.is_admin:
      print(f"User {user} is already admin.", file=sys.stderr)
    else:
      user.is_admin = True
      user.save()
      print(f"User {user} added to admin list.")
  else:
    print(f"User {user} not found", file=sys.stderr)

@admin.command("revoke")
@argument("user", type=str)
@pass_obj
def revoke_admin(ctx, user):
  if user := User.query.filter_by(username=user).first():
    if not user.is_admin:
      print(f"User {user} was not already admin.", file=sys.stderr)
    else:
      user.is_admin = False
      user.save()
      print(f"User {user} removed from admin list.")
  else:
    print(f"User {user} not found", file=sys.stderr)
