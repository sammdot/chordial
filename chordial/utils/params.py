from flask_restful import abort
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import FlaskParser


class Parser(FlaskParser):
  def _handle_invalid_json_error(self, error, req, *args, **kwargs):
    abort(HTTPStatus.BAD_REQUEST, message="Invalid JSON body")

  def handle_error(
    self, error, req, schema, *, error_status_code, error_headers
  ):
    abort(
      HTTPStatus.BAD_REQUEST,
      message="Invalid request",
      errors=error.messages.get("json", error.messages.get("query")),
    )


parser = Parser()


def params(**kwargs):
  return parser.use_kwargs(kwargs, location="query")


def json_params(**kwargs):
  return parser.use_kwargs(kwargs, location="json")
