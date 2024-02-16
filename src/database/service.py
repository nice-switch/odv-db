import peewee

from database import model, interface

class DatabaseService():
    def __init__(self, sqlite_path: str | None = None):
        # SQLite value initialization.
        self.sqlite_path: str | None = sqlite_path
        self.sqlite_connection: peewee.SqliteDatabase | None = None

        # Does a SQLite path exist?
        if sqlite_path is not None:
            # Create SQLite connection.
            self.sqlite_connection = peewee.SqliteDatabase(sqlite_path)

            # Add SQLite connection to database proxy.
            model.database_connection.initialize(self.sqlite_connection)

            # Create tables for the new database instance.
            self.sqlite_connection.create_tables(model.AVAILABLE_MODELS)
            self.sqlite_connection.commit()
    

    def create_account(self, username: str, password: str) -> interface.AccountInterface | None:
        # Checking if an account already exists with this username.
        if self.get_account(username=username):
            return None

        # Create an account in the database.
        # NOTE this is prob not the best thing to do but it works!
        model.database_connection.initialize(self.sqlite_connection)
        model.Account.create(username=username, password=password, salt="", blob="")
            
        return interface.AccountInterface(
            account_model=self.get_account(
                username=username,
            ),
            new_account=True
        )
    

    def get_account(self, username: str) -> interface.AccountInterface | None:
        account_model: model.Account | None = None

        # Attempting to retrieve account from database.
        try:
            # TODO this is prob not good but it works!
            model.database_connection.initialize(self.sqlite_connection)
            account_model = model.Account.get(model.Account.username==username)
        except Exception as _:
            pass
        
        # If account is found create interface!
        if account_model is not None:
            return interface.AccountInterface(
                account_model=account_model
            )

        return None