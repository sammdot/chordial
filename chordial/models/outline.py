from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship

from chordial.models.base import Base, BaseSchema
from chordial.models.layout import Layout
from chordial.models.mixins import id_mixin

class Outline(Base, id_mixin(8)):
  __tablename__ = "outlines"

  layout_id = Column(BigInteger,
    ForeignKey("layouts.id", ondelete="RESTRICT"), nullable=False)
  steno = Column(String, nullable=False)

  layout = relationship("Layout")

  __table_args__ = (
    UniqueConstraint("layout_id", "steno", name="unique_outline_per_layout"),
  )

  @property
  def repr_label(self):
    return self.steno

class OutlineSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Outline

Outline.schema = OutlineSchema()
