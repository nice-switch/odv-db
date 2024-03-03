import database


# Hear me out, we make it again but simpler and less convolution/abstraction maybe?
# Idk im gonna wing it.

sqlite_connection = database.model.peewee.SqliteDatabase(":memory:")
database.model.change_database_to(sqlite_connection, create_tables=True)


new_account = database.create_account(
    username="john_doe",
    password="password123"
)

print('init passwd check', new_account.decrypt_data("password123"))
print('password changed!', new_account.update_password("testpassword", "password123"))
print('trying old password', new_account.decrypt_data("password123"))
print('trying new password', new_account.decrypt_data("testpassword"))