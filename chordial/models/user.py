from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import joinedload
from sqlalchemy.schema import CheckConstraint
from sqlalchemy_utils import EmailType as Email, PasswordType as Password

from chordial.models.base import Base, BaseSchema
from chordial.models.enums import Visibility
from chordial.models.mixins import IdMixin, TimestampMixin
from chordial.utils.datetime import minutes_from_now
from chordial.utils.uid import generate_verify_token


class User(Base, IdMixin(6), TimestampMixin):
  __tablename__ = "users"

  username = Column(String, nullable=False, unique=True)
  display_name = Column(String)
  email = Column(Email, nullable=False)
  email_verified = Column(Boolean, default=False)
  email_verify_token = Column(String, default=generate_verify_token)
  email_verify_expiry_time = Column(
    DateTime(timezone=True), default=minutes_from_now(15)
  )
  is_admin = Column(Boolean, default=False)
  is_system = Column(Boolean, default=False)
  password = Column(Password(schemes=["pbkdf2_sha512"]))

  @property
  def public_dictionaries(self):
    return (d for d in self.dictionaries if d.visibility == Visibility.public)

  __table_args__ = (
    CheckConstraint(
      "email_verified OR (email_verify_token IS NOT NULL "
      "AND email_verify_expiry_time IS NOT NULL)",
      name="verify_token_check",
    ),
    CheckConstraint(
      "is_system OR password IS NOT NULL", name="non_system_password_check"
    ),
  )

  @property
  def short_name(self):
    return self.username

  @staticmethod
  def with_id(id: int):
    return (
      User.query.options(joinedload(User.dictionaries)).filter_by(id=id).first()
    )

  @staticmethod
  def with_username(username: str):
    return (
      User.query.options(joinedload(User.dictionaries))
      .filter(User.username.ilike(f"%{username}%"))
      .first()
    )

  @staticmethod
  def all():
    return User.query.all()


class UserAuthSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = User
    exclude = BaseSchema.Meta.exclude + (
      "password",
      "email_verify_token",
      "email_verify_expiry_time",
    )


class UserFullSchema(UserAuthSchema):
  dictionaries = Nested("DictionarySchema", many=True, exclude=("user",))


class UserSchema(UserAuthSchema):
  dictionaries = Nested(
    "DictionarySchema",
    attribute="public_dictionaries",
    many=True,
    exclude=("user",),
  )


class UserVerifySchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = User
    exclude = BaseSchema.Meta.exclude + ("password", "email_verified")

  needs_verification = fields.Function(lambda obj: not obj.email_verified)


User.schema = UserSchema()
User.full_schema = UserFullSchema()
User.auth_schema = UserAuthSchema()
User.verify_schema = UserVerifySchema()
