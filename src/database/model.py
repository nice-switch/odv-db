import peewee

database_connection: peewee.Proxy = peewee.Proxy()


# BaseModel for other classes to inherit.
class BaseModel(peewee.Model):
    class Meta:
        database = database_connection


# Account model.
class Account(BaseModel):
    username = peewee.TextField(unique=True, primary_key=True, index=True)
    password = peewee.TextField(default="")
    email = peewee.TextField(default="")
    nonce = peewee.TextField(default="")
    blob = peewee.TextField(default="")
    salt = peewee.TextField(default="")


# TODO blob table for obscuring data between multiple accounts.
    

# NOTE MUST USE THIS FUNCTION WHEN CHANGING DATABASE AT ALL TIMES! PLEASE FUTURE ME BE CONSISTENT!
# TODO change how this works, add custom funcs that create the databases and change the input values to be ID/Name based.
def change_database_to(target_database: peewee.Database, create_tables: bool | None = False):
    """Changes the database that peewee is interacting with.

    Args:   
        target_database (peewee.Database): peewee.SqliteDatabase, peewee.PostgresqlDatabase, etc,.
        create_tables (bool | None): If it should use .create_tables([...])
    """
    database_connection.initialize(target_database)

    if create_tables:
        database_connection.create_tables([
            Account
        ])

        database_connection.commit()