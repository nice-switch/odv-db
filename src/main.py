import database


database_service_a = database.service.DatabaseService(
    sqlite_path=":memory:" #"workspace/database.sqlite"
)

database_service_b = database.service.DatabaseService(
    sqlite_path=":memory:"#"workspace/test.sqlite"
)

account_a = database_service_a.create_account(
    username="dees nuts",
    password="bruh"
)

account_b = database_service_b.create_account(
    username="test",
    password="account"
)

print(account_b.get_username())