from peewee import *

database = SqliteDatabase(None)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SeasonsTypes(BaseModel):
    name = TextField()
    description = TextField(null=True)

    class Meta:
        table_name = 'SeasonsTypes'

class Series(BaseModel):
    sort_id = IntegerField()
    name = TextField(null=True)
    description = TextField(null=True)
    is_deleted = BareField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'Series'

class Seasons(BaseModel):
    sort_id = IntegerField()
    name = TextField(null=True)
    date = TextField(null=True)
    serie = ForeignKeyField(column_name='serie', field='id', model=Series)
    type = ForeignKeyField(column_name='type', field='id', model=SeasonsTypes, null=True)
    studio = IntegerField(index=True, null=True)
    is_deleted = BareField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'Seasons'

class Planning(BaseModel):
    season = ForeignKeyField(column_name='season', field='id', model=Seasons)
    date = DateField()
    episode = IntegerField()

    class Meta:
        table_name = 'Planning'

class Studios(BaseModel):
    name = TextField(null=True)

    class Meta:
        table_name = 'Studios'

class TagsGroups(BaseModel):
    name = TextField(null=True)
    color = TextField(null=True)

    class Meta:
        table_name = 'TagsGroups'

class Tags(BaseModel):
    name = TextField(null=True)
    tags_group = ForeignKeyField(column_name='tags_group', field='id', model=TagsGroups, null=True)

    class Meta:
        table_name = 'Tags'

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

