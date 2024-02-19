import peewee

database_connection: peewee.Proxy = peewee.Proxy()

class BaseModel(peewee.Model):
    class Meta:
        database = database_connection


class Account(BaseModel):
    username = peewee.TextField(primary_key=True, index=True, unique=True)
    password = peewee.TextField()
    nonce = peewee.TextField()
    salt = peewee.TextField()
    blob = peewee.TextField()


class Data(BaseModel):
    id = peewee.TextField(primary_key=True, index=True, unique=True)
    blob = peewee.TextField()


AVAILABLE_MODELS = [Account, Data]