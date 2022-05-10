from marshmallow.fields import Pluck
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship

from chordial.models.base import Base, BaseSchema
from chordial.models.enums import DerivationType, EntryStatus
from chordial.models.dictionary import Dictionary
from chordial.models.outline import Outline
from chordial.models.translation import Translation
from chordial.models.mixins import id_mixin

class Entry(Base, id_mixin(10)):
  __tablename__ = "entries"

  dictionary_id = Column(Integer, ForeignKey("dictionaries.id"), nullable=False)
  outline_id = Column(Integer, ForeignKey("outlines.id"), nullable=False)
  translation_id = Column(Integer, ForeignKey("translations.id"), nullable=False)

  dictionary = relationship("Dictionary", backref="entries")
  outline = relationship("Outline", backref="entries")
  translation = relationship("Translation", backref="entries")

  status = Column(Enum(EntryStatus), default=EntryStatus.unknown)
  derivation = Column(Enum(DerivationType), default=DerivationType.unknown)
  mnemonic = Column(String)

  __table_args__ = (
    UniqueConstraint(
      "dictionary_id", "outline_id", name="unique_outline_per_dictionary"),
  )

  @property
  def repr_label(self):
    return f"{self.outline.repr_label} => {self.translation.repr_label}"

class EntrySchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Entry

  outline = Nested("OutlineSchema")
  translation = Nested("TranslationSchema")
  status = EnumField(EntryStatus)
  derivation = EnumField(DerivationType)

class EntryListSchema(BaseSchema):
  class Meta(BaseSchema.Meta):
    model = Entry
    exclude = BaseSchema.Meta.exclude + ("derivation", "mnemonic")

  steno = Pluck("OutlineSchema", "steno", attribute="outline")
  translation = Pluck("TranslationSchema", "translation")
  status = EnumField(EntryStatus)

Entry.schema = EntrySchema()
Entry.list_schema = EntryListSchema()