from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import Column, String

from chordial.models.base import Base, BaseSchema
from chordial.models.mixins import id_mixin

class Layout(Base, id_mixin(4)):
  __tablename__ = "layouts"

  short_name = Column(String, nullable=False, unique=True)
  display_name = Column(String, nullable=False, unique=True)

  @staticmethod
  def with_id(id: int):
    return Layout.query.filter_by(id=id).first()

  @staticmethod
  def with_short_name(short_name: str):
    return Layout.query.filter_by(short_name=short_name).first()

  @staticmethod
  def all():
    return Layout.query.all()

class LayoutSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Layout

  theories = Nested("TheorySchema", many=True, exclude=("layout",))

Layout.schema = LayoutSchema()
