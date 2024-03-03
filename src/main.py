import database


# Hear me out, we make it again but simpler and less convolution/abstraction maybe?
# Idk im gonna wing it.

sqlite_connection = database.model.peewee.SqliteDatabase("workspace/database.sqlite")
database.model.change_database_to(sqlite_connection, create_tables=True)

account = database.create_account(
    username="john_doe",
    password="password123"
) or database.get_account("john_doe")


print("Data Update Successful?", account.update_data("password123", {"dees": "nuts"}))
print("Decryption attempt: ", account.decrypt_data("password123"))
