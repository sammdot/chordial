from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from chordial.models.base import Base, BaseSchema
from chordial.models.layout import Layout
from chordial.models.mixins import IdMixin

class Theory(Base, IdMixin(4)):
  __tablename__ = "theories"

  short_name = Column(String, nullable=False, unique=True)
  display_name = Column(String, nullable=False, unique=True)
  layout_id = Column(BigInteger,
    ForeignKey("layouts.id", ondelete="RESTRICT"), nullable=False)
  official_dictionary_id = Column(BigInteger,
    ForeignKey("dictionaries.id", ondelete="SET NULL"))

  layout = relationship("Layout", backref="theories")

  @staticmethod
  def with_id(id: int):
    return Theory.query.filter_by(id=id).first()

  @staticmethod
  def with_short_name(short_name: str):
    return Theory.query.filter_by(short_name=short_name).first()

  @staticmethod
  def all():
    return Theory.query.all()

class TheorySchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Theory

  layout = Nested("LayoutSchema", exclude=("theories",))
  official_dictionary = Nested(
    "DictionarySchema", exclude=("user", "layout", "theory"))

Theory.schema = TheorySchema()
