from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchemaOpts
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseSchema(SQLAlchemyAutoSchema):
  class Meta:
    exclude = ("id",)
    load_instance = True

  uid = fields.Str(dump_only=True)
