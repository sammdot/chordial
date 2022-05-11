from marshmallow_enum import EnumField
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import BigInteger, Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import UniqueConstraint

from chordial.models.base import Base, BaseSchema
from chordial.models.enums import Visibility
from chordial.models.layout import Layout
from chordial.models.mixins import IdMixin, TimestampMixin
from chordial.models.user import User

class Dictionary(Base, IdMixin(6), TimestampMixin):
  __tablename__ = "dictionaries"

  name = Column(String, nullable=False)
  display_name = Column(String)
  layout_id = Column(BigInteger,
    ForeignKey("layouts.id", ondelete="RESTRICT"), nullable=False)
  user_id = Column(BigInteger,
    ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  visibility = Column(Enum(Visibility), default=Visibility.public)
  proprietary = Column(Boolean, default=False)

  layout = relationship("Layout")
  user = relationship("User", backref=backref(
    "dictionaries", cascade="all, delete-orphan", passive_deletes=True))

  __table_args__ = (
    UniqueConstraint("user_id", "name", name="unique_per_user"),
  )

  @property
  def short_name(self):
    return f"{self.user.username}/{self.name}"

  @staticmethod
  def with_id(id: int):
    return Dictionary.query.filter_by(id=id).first()

  @staticmethod
  def with_name(username: str, name: str):
    if u := User.with_username(username):
      return Dictionary.query.filter_by(user_id=u.id, name=name).first()

class DictionarySchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Dictionary

  visibility = EnumField(Visibility)
  layout = Nested("LayoutSchema", exclude=("theories",))
  user = Nested("UserSchema", exclude=("dictionaries",))
  theory = Nested("TheorySchema", exclude=("official_dictionary", "layout"))

class DictionaryFullSchema(DictionarySchema):
  entries = Nested("EntryListSchema", many=True)

Dictionary.schema = DictionarySchema()
Dictionary.full_schema = DictionaryFullSchema()
