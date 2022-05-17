from marshmallow_sqlalchemy.fields import Nested
from plover_stroke import BaseStroke
from sqlalchemy import Column, String
from sqlalchemy_utils import JSONType as JSON

from chordial.models.base import Base, BaseSchema
from chordial.models.mixins import IdMixin

STROKE_SEPARATOR = "/"

class Layout(Base, IdMixin(4)):
  __tablename__ = "layouts"

  short_name = Column(String, nullable=False, unique=True)
  display_name = Column(String, nullable=False, unique=True)

  system_definition = Column(JSON, nullable=False)

  _Stroke = None

  @property
  def stroke_parser(self):
    if self._Stroke:
      return self._Stroke
    class Stroke(BaseStroke):
      pass
    Stroke.setup(**self.system_definition, feral_number_key=True)
    self._Stroke = Stroke
    return Stroke

  def normalize(self, outline):
    return STROKE_SEPARATOR.join([
      str(self.stroke_parser.from_steno(stroke))
      for stroke in outline.split(STROKE_SEPARATOR)])

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
    exclude = BaseSchema.Meta.exclude + ("system_definition",)

  theories = Nested("TheorySchema", many=True, exclude=("layout",))

Layout.schema = LayoutSchema()
