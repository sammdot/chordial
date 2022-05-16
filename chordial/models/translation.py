from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from chordial.models.base import Base, BaseSchema
from chordial.models.mixins import IdMixin

class Translation(Base, IdMixin(8)):
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

  @staticmethod
  def with_id(id):
    return Translation.query.filter_by(id=id).first()

  @staticmethod
  def with_text(text, layout):
    return Translation.query.filter_by(layout=layout, translation=text).first()

class TranslationSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Translation

class TranslationFullSchema(TranslationSchema):
  layout = Nested("LayoutSchema")

Translation.schema = TranslationSchema()
Translation.full_schema = TranslationFullSchema()
