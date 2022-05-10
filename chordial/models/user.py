from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested
from passlib.hash import pbkdf2_sha256 as password_hash
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import joinedload

from chordial.models.base import Base, BaseSchema
from chordial.models.enums import Visibility
from chordial.models.mixins import id_mixin

class User(Base, id_mixin(6)):
  __tablename__ = "users"

  username = Column(String, nullable=False, unique=True)
  display_name = Column(String)
  is_admin = Column(Boolean, default=False)
  is_system = Column(Boolean, default=False)
  password = Column(String, nullable=False)

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
  def new(username, password):
    u = User(username=username, password=password_hash.hash(password))
    u.save()
    return u

  def verify_password(self, password):
    return password_hash.verify(password, self.password)

class UserAuthSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = User
    exclude = BaseSchema.Meta.exclude + ("password",)

class UserFullSchema(UserAuthSchema):
  dictionaries = Nested(
    "DictionarySchema",
    many=True, exclude=("entries", "user"))

class UserSchema(UserAuthSchema):
  dictionaries = Nested(
    "DictionarySchema", attribute="public_dictionaries",
    many=True, exclude=("entries", "user"))

User.schema = UserSchema()
User.full_schema = UserFullSchema()
User.auth_schema = UserAuthSchema()
