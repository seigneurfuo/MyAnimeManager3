from peewee import *

database = SqliteDatabase('database2.sqlite3')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Series(BaseModel):
    id_ = AutoField(null=True)
    sort_id = IntegerField()
    name = CharField(null=True)
    description = CharField(null=True)

    class Meta:
        table_name = 'Series'

class Seasons(BaseModel):
    id_ = AutoField(null=True)
    sort_id = IntegerField()
    name = CharField(null=True)
    serie = ForeignKeyField(column_name='serie', field='id_', model=Series)

    class Meta:
        table_name = 'Seasons'

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

