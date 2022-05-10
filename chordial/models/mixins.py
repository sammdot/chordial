from sqlalchemy import Column, Integer, String

from chordial.utils.uid import encode, generate_id

def id_mixin(length: int):
  class IdMixin:
    id = Column(Integer, primary_key=True, default=lambda: generate_id(length))

    def __repr__(self):
      return f"<{type(self).__name__} {self.repr_label} ({self.uid})>"

    @property
    def uid(self):
      return encode(self.id, length)

    @property
    def short_name(self):
      return self.uid

    @property
    def repr_label(self):
      return self.short_name

  return IdMixin
