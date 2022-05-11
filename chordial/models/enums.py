from enum import Enum

class Visibility(Enum):
  public = 1
  unlisted = 2
  private = 3

class EntryStatus(Enum):
  misstroke = -1
  unknown = 0
  correct = 1
  preferred = 2
  recommended = 3
  mandatory = 4

class DerivationType(Enum):
  arbitrary = -1
  unknown = 0
  phonetic = 1
  semi_phonetic = 2
  skeletal = 3
  shape_based = 4

class DictionaryFormat(Enum):
  json = 0
