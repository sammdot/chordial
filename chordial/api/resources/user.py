from http import HTTPStatus
from flask import g, redirect
from flask_restful import abort, Resource, url_for

from chordial.models import User
from chordial.utils.datetime import now
from chordial.utils.params import fields, json_params, params


class UserResource(Resource):
  def get(self, user_id):
    if u := User.with_id(user_id):
      if g.id == user_id or g.is_admin:
        return User.full_schema.dump(u)
      else:
        return User.schema.dump(u)
    abort(HTTPStatus.NOT_FOUND, message=f"No user with ID {user_id}")


class UsersResource(Resource):
  @params(name=fields.Str())
  def get(self, name=None):
    if name:
      if u := User.with_username(name):
        return redirect(url_for("user", user_id=u.id))
      abort(HTTPStatus.NOT_FOUND, message=f"User {name} does not exist")
    elif g.is_admin:
      return [User.schema.dump(u) for u in User.all()]
    else:
      abort(HTTPStatus.FORBIDDEN, message=f"Admin permissions required")

  @json_params(
    username=fields.Str(required=True),
    email=fields.Str(required=True),
    password=fields.Str(required=True),
  )
  def post(self, username, email, password):
    if u := User.with_username(username):
      abort(HTTPStatus.BAD_REQUEST, message=f"User {username} already exists")
    if u := User.query.filter_by(email=email).first():
      abort(
        HTTPStatus.BAD_REQUEST,
        message=f"User with email {email} already exists",
      )
    u = User(username=username, email=email, password=password)
    u.save()
    # TODO: Send email with verification token
    return User.verify_schema.dump(u)


class UserVerifyResource(Resource):
  @json_params(
    email=fields.Str(required=True),
    verify_token=fields.Str(required=True),
  )
  def post(self, user_id, email, verify_token):
    if u := User.with_id(user_id):
      if u.email_verified:
        abort(HTTPStatus.BAD_REQUEST, message="Already verified")
      if u.email != email:
        abort(HTTPStatus.BAD_REQUEST, message="Invalid email")
      if u.email_verify_token != verify_token:
        abort(HTTPStatus.BAD_REQUEST, message="Invalid verify token")
      if u.email_verify_expiry_time < now():
        abort(HTTPStatus.BAD_REQUEST, message="Expired verify token")
      u.email_verified = True
      u.email_verify_token = None
      u.email_verify_expiry_time = None
      u.save()
      return User.verify_schema.dump(u)
    abort(HTTPStatus.NOT_FOUND, message=f"No user with ID {user_id}")
