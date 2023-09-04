import time

from tinydb import TinyDB, Query
from pathlib import Path

userdb = TinyDB(Path("data/per-instance/userdb.json"))
templatedb = TinyDB(Path("data/per-instance/templatedb.json"))


class DatabaseError(LookupError):
    pass


class NotInDatabaseError(DatabaseError):
    pass


class AlreadyInDatabaseError(DatabaseError):
    pass


def create_new_user(discord_id: int):
    User = Query()
    if userdb.contains(User.id == discord_id):
        raise AlreadyInDatabaseError
    else:
        userdb.insert({"id": discord_id})


def create_new_template(creator_id: int, name: str, template: str):
    Template = Query()
    if userdb.contains(Template.name == name):
        raise AlreadyInDatabaseError
    else:
        userdb.insert({"creator_id": id, "name": name, "template": template,
                       "created": time.time_ns(), "updated": time.time_ns()})


def edit_template(creator_id: int, name: str, template: str):
    Template = Query()
    if userdb.contains(Template.name == name):
        userdb.update({"template": template, "updated": time.time_ns()}, Template.name == name)
    else:
        raise NotInDatabaseError
