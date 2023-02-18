from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase

db = SqliteQueueDatabase("by002.db")

class Users(Model):
    user_id = BigIntegerField(default=0)
    username = TextField(default="")
    dick = IntegerField(default=0)
    end_date = TextField(default="")
    chat_id = BigIntegerField(default=0)

    class Meta:
        db_table = "Users"
        database = db


def connect():
    db.connect()
    Users.create_table()