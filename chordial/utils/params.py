from webargs import fields
from webargs.flaskparser import use_kwargs

def params(**kwargs):
  return use_kwargs(kwargs, location="query")

def json_params(**kwargs):
  return use_kwargs(kwargs, location="json")
