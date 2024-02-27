import database


# Hear me out, we make it again but simpler and less convolution/abstraction maybe?
# Idk im gonna wing it.

sqlite_connection = database.model.peewee.SqliteDatabase(":memory:")#"workspace/database.sqlite")
database.model.change_database_to(sqlite_connection, create_tables=True)


new_account = database.create_account(
    username="john_doe",
    password="password123"
)

print(new_account)
print(new_account.decrypt_data("password123"))