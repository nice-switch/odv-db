import database



database_service_a = database.service.DatabaseService(
    sqlite_path="workspace/database.sqlite"
)

database_service_b = database.service.DatabaseService(
    sqlite_path="workspace/test.sqlite"
)

database_service_a.create_account(
    username="dees nuts",
    password="bruh"
)

database_service_b.create_account(
    username="test",
    password="account"
)