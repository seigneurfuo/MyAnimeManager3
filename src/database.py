from peewee import *

database = SqliteDatabase(None)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Series(BaseModel):
    id_ = AutoField()
    sort_id = IntegerField()
    name = TextField(null=True)
    description = TextField(null=True)
    is_deleted = BareField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'Series'

class Studios(BaseModel):
    id_ = AutoField()
    name = TextField(null=True)

    class Meta:
        table_name = 'Studios'

class SeasonsTypes(BaseModel):
    id_ = AutoField()
    name = TextField()
    description = TextField(null=True)

    class Meta:
        table_name = 'SeasonsTypes'

class Seasons(BaseModel):
    id_ = AutoField()
    sort_id = IntegerField()
    name = TextField(null=True)
    date = TextField(null=True)
    serie = ForeignKeyField(column_name='serie', field='id_', model=Series)
    seasons_type = ForeignKeyField(column_name='seasons_type', field='id_', model=SeasonsTypes, null=True)
    studio = ForeignKeyField(column_name='studio', field='id_', model=Studios, null=True)
    is_deleted = BareField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'Seasons'

class TagsGroups(BaseModel):
    id_ = IntegerField(null=True)
    name = TextField(null=True)
    color = TextField(null=True)

    class Meta:
        table_name = 'TagsGroups'
        primary_key = False

class Tags(BaseModel):
    id_ = IntegerField(null=True)
    name = TextField(null=True)
    tags_group = ForeignKeyField(column_name='tags_group', field='id_', model=TagsGroups, null=True)

    class Meta:
        table_name = 'Tags'
        primary_key = False

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

