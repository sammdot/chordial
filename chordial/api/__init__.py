from flask_restful import Api

from chordial.api.resources import (
  AuthResource,
  DictionaryEntriesResource,
  DictionaryResource, DictionariesResource,
  EntryResource, EntryByIdsResource, EntriesResource,
  LayoutResource, LayoutsResource,
  OutlineResource,
  TheoryResource, TheoriesResource,
  TranslationResource,
  UserResource, UsersResource, UserVerifyResource,
)

api = Api(catch_all_404s=True)

api.add_resource(AuthResource, "/auth")
api.add_resource(DictionaryEntriesResource, "/dicts/<uid6:dict_id>/entries", endpoint="dict_entries")
api.add_resource(DictionaryResource, "/dicts/<uid6:dict_id>", endpoint="dict")
api.add_resource(DictionariesResource, "/dicts")
api.add_resource(EntryResource, "/entries/<uid10:entry_id>", endpoint="entry")
api.add_resource(EntryByIdsResource, "/entries/<uid8:outline_id>/<uid8:translation_id>")
api.add_resource(EntriesResource, "/entries")
api.add_resource(LayoutResource, "/layouts/<uid4:layout_id>", endpoint="layout")
api.add_resource(LayoutsResource, "/layouts")
api.add_resource(OutlineResource, "/outlines/<uid8:outline_id>", endpoint="outline")
api.add_resource(TheoryResource, "/theories/<uid4:theory_id>", endpoint="theory")
api.add_resource(TheoriesResource, "/theories")
api.add_resource(TranslationResource, "/translations/<uid8:translation_id>", endpoint="translation")
api.add_resource(UserResource, "/users/<uid6:user_id>", endpoint="user")
api.add_resource(UserVerifyResource, "/users/<uid6:user_id>/verify")
api.add_resource(UsersResource, "/users")
