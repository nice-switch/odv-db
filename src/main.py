import database


# Hear me out, we make it again but simpler and less convolution/abstraction maybe?
# Idk im gonna wing it.

print(database.secure.hash_password("apsodigjadspogiha", num_hashes=2))

"""
database_service = database.service.DatabaseService(
    sqlite_path=":memory:"#"workspace/database.sqlite"
)

account_handler = database_service.create_account(
    username="test",
    password="account"
)

print(account_handler.get_nonce())

print(account_handler.get_blob().decrypt_blob(
    "account",
    bytes.fromhex(account_handler.get_salt()),
    bytes.fromhex(account_handler.get_nonce())
).decode())
"""