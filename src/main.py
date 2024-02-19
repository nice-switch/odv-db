import database


database_service = database.service.DatabaseService(
    sqlite_path="workspace/database.sqlite"
)

account_handler = database_service.create_account(
    username="test",
    password="account"
)

print(account_handler.get_username())