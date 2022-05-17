from marshmallow import fields
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from chordial.models.base import Base, BaseSchema
from chordial.models.layout import Layout
from chordial.models.mixins import IdMixin

class Outline(Base, IdMixin(8)):
  __tablename__ = "outlines"

  layout_id = Column(BigInteger,
    ForeignKey("layouts.id", ondelete="RESTRICT"), nullable=False)
  steno = Column(String, nullable=False)

  layout = relationship("Layout")

  __table_args__ = (
    UniqueConstraint("layout_id", "steno", name="unique_outline_per_layout"),
  )

  @property
  def steno_without_number(self):
    return self.layout.normalize_remove_number(self.steno)

  @property
  def repr_label(self):
    return self.steno

  @staticmethod
  def with_id(id):
    return Outline.query.filter_by(id=id).first()

  @staticmethod
  def with_steno(steno, layout):
    return Outline.query.filter_by(layout=layout, steno=steno).first()

class OutlineSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Outline

  steno_without_number = fields.Str()

class OutlineFullSchema(OutlineSchema):
  layout = Nested("LayoutSchema")

Outline.schema = OutlineSchema()
Outline.full_schema = OutlineFullSchema()
