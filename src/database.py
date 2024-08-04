from playhouse.sqlite_ext import *

database = SqliteExtDatabase(None)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class SeasonsTypes(BaseModel):
    sort_id = IntegerField()
    name = TextField()
    description = TextField(null=True)

    class Meta:
        table_name = 'SeasonsTypes'


class Series(BaseModel):
    sort_id = IntegerField()
    name = TextField()
    description = TextField(null=True)
    path = TextField(null=True)
    picture = BlobField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'Series'


class Seasons(BaseModel):
    sort_id = IntegerField()
    name = TextField()
    year = IntegerField(null=True)
    airing = BooleanField(null=False, default=True)
    serie = ForeignKeyField(column_name='serie', field='id', model=Series, backref="seasons")
    type = ForeignKeyField(column_name='type', field='id', model=SeasonsTypes, null=True)
    studio = IntegerField(index=True, null=True)
    episodes = IntegerField()
    watched_episodes = IntegerField()
    view_count = IntegerField()
    state = IntegerField()
    rating = IntegerField(null=True)
    description = TextField()
    custom_data = JSONField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'Seasons'


class Planning(BaseModel):
    serie = ForeignKeyField(column_name='serie', field='id', model=Series)
    season = ForeignKeyField(column_name='season', field='id', model=Seasons)
    date = DateField()
    episode = IntegerField()

    class Meta:
        table_name = 'Planning'


class Friends(BaseModel):
    name = TextField()

    class Meta:
        table_name = 'Friends'


class FriendsPlanning(BaseModel):
    friend = ForeignKeyField(column_name='friend', field='id', model=Friends, null=True, backref='plannings')
    planning = ForeignKeyField(column_name='planning', field='id', model=Planning, null=True, backref='friends')

    class Meta:
        table_name = 'FriendsPlanning'
