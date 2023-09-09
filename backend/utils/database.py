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


class DatabasePermissionsError(DatabaseError):
    pass


def create_new_user(discord_id: int):
    User = Query()
    if userdb.contains(User.id == discord_id):
        raise AlreadyInDatabaseError
    else:
        userdb.insert({"id": discord_id})


def create_new_tag(creator_id: int, name: str, template: str):
    Tag = Query()
    if templatedb.contains(Tag.name == name):
        raise AlreadyInDatabaseError
    else:
        templatedb.insert({"creator_id": creator_id, "name": name, "template": template,
                           "created": time.time_ns(), "updated": time.time_ns(), "uses": 0})


def edit_tag(creator_id: int, name: str, template: str):
    Tag = Query()
    if templatedb.contains(Tag.name == name):
        if creator_id == get_tag_by_name(name)["creator_id"]:
            templatedb.update({"template": template, "updated": time.time_ns()}, Tag.name == name)
        else:
            raise DatabasePermissionsError
    else:
        raise NotInDatabaseError


def increment_tag_uses(name: str):
    Tag = Query()
    if templatedb.contains(Tag.name == name):
        templatedb.update({"uses": (get_tag_by_name(name)["uses"] + 1)}, Tag.name == name)
    else:
        raise NotInDatabaseError


def get_tag_by_name(name: str):
    Tag = Query()
    if templatedb.contains(Tag.name == name):
        return templatedb.get(Tag.name == name)
    else:
        raise NotInDatabaseError
