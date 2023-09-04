from tinydb import TinyDB
from pathlib import Path
userdb = TinyDB(Path("data/per-instance/userdb.json"))

def create_new_user(id: int):
    userdb.insert({"id": id})