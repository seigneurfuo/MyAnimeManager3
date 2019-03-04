from peewee import *

database = SqliteDatabase('database.sqlite3', **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Series(BaseModel):
    name = TextField(null=True)
    sort_id = IntegerField()

    class Meta:
        table_name = 'Series'

class Seasons(BaseModel):
    name = TextField()
    serie = ForeignKeyField(column_name='serie', field='id', model=Series)
    sort_id = IntegerField()

    class Meta:
        table_name = 'Seasons'

class SqliteSequence(BaseModel):
    name = UnknownField(null=True)  # 
    seq = UnknownField(null=True)  # 

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

