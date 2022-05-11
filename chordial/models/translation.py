from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship

from chordial.models.base import Base, BaseSchema
from chordial.models.mixins import id_mixin

class Translation(Base, id_mixin(8)):
  __tablename__ = "translations"

  layout_id = Column(BigInteger,
    ForeignKey("layouts.id", ondelete="RESTRICT"), nullable=False)
  translation = Column(String, nullable=False)
  spelling_variant = Column(String)

  layout = relationship("Layout")

  __table_args__ = (
    UniqueConstraint(
      "layout_id", "translation", name="unique_translation_per_layout"),
  )

  @property
  def repr_label(self):
    return f"'{self.translation}'"

class TranslationSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Translation

Translation.schema = TranslationSchema()
