from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import joinedload
from sqlalchemy_utils import EmailType as Email, PasswordType as Password

from chordial.models.base import Base, BaseSchema
from chordial.models.enums import Visibility
from chordial.models.mixins import IdMixin, TimestampMixin

class User(Base, IdMixin(6), TimestampMixin):
  __tablename__ = "users"

  username = Column(String, nullable=False, unique=True)
  display_name = Column(String)
  email = Column(Email, nullable=False)
  email_verified = Column(Boolean, default=False)
  is_admin = Column(Boolean, default=False)
  is_system = Column(Boolean, default=False)
  password = Column(Password(schemes=["pbkdf2_sha512"]), nullable=False)

  @property
  def public_dictionaries(self):
    return (d for d in self.dictionaries if d.visibility == Visibility.public)

  @property
  def short_name(self):
    return self.username

  @staticmethod
  def with_id(id: int):
    return User.query.options(joinedload(User.dictionaries)).filter_by(id=id).first()

  @staticmethod
  def with_username(username: str):
    return User.query.options(joinedload(User.dictionaries)).filter_by(username=username).first()

  @staticmethod
  def all():
    return User.query.all()

class UserAuthSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = User
    exclude = BaseSchema.Meta.exclude + ("password",)

class UserFullSchema(UserAuthSchema):
  dictionaries = Nested(
    "DictionarySchema", many=True, exclude=("user",))

class UserSchema(UserAuthSchema):
  dictionaries = Nested(
    "DictionarySchema", attribute="public_dictionaries",
    many=True, exclude=("user",))

User.schema = UserSchema()
User.full_schema = UserFullSchema()
User.auth_schema = UserAuthSchema()
