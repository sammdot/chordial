import random
import string
from werkzeug.routing import BaseConverter, ValidationError

ALPHABET = string.digits + string.ascii_lowercase
BASE = len(ALPHABET)
LENGTH = 8

def encode(id: int, length=LENGTH) -> str:
  s = ""
  num = id
  while num:
    s = ALPHABET[num % BASE] + s
    num //= BASE
  return s.rjust(length, "0")

def decode(id: str) -> int:
  return int(id, base=BASE)

def generate_id(length=LENGTH) -> int:
  return decode("".join(random.choices(ALPHABET, k=length)))

def uid_converter(length: int):
  class UniqueIdConverter(BaseConverter):
    def to_python(self, value: str) -> int:
      return decode(value)

    def to_url(self, value: int) -> str:
      return encode(value, length)

  return UniqueIdConverter
