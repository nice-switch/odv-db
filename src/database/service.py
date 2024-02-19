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
            self.__override_database_connection_with_self() #model.database_connection.initialize(self.sqlite_connection)

            # Create tables for the new database instance.
            self.sqlite_connection.create_tables(model.AVAILABLE_MODELS)
            self.sqlite_connection.commit()
    

    def create_account(self, username: str, password: str) -> interface.AccountInterface | None:
        """Top level interface for creating an account.

        Args:
            username (str): Target username for the new account.
            password (str): Raw password for the account.

        Raises:
            Exception: If an account already exists.
            Exception: If the username fails the username requirements.

        Returns:
            interface.AccountInterface | None: AccountInterface if successfully created.
        """
        # TODO username requirements check

        # Checking if an account already exists with this username.
        if self.get_account(username=username):
            raise Exception("An account already exists with that username!")

        # Create an account in the database.
        # NOTE this is prob not the best thing to do but it works!
        self.__override_database_connection_with_self() #model.database_connection.initialize(self.sqlite_connection)

        # Creating the account! OMG!
        account_model =  model.Account.create(username=username, password=password, salt="", blob="")
        
        # Wrapping the account model in an interface for easy handling!
        return interface.AccountInterface(
            account_model=account_model
        )
    

    def get_account(self, username: str) -> interface.AccountInterface | model.Account | None:
        """Top level interface for retrieving an account.

        Args:
            username (str): Target username of the account you want to find.

        Returns:
            interface.AccountInterface | None: If it doesn't find an account it will return None.
        """
        account_model: model.Account | None = None

        # Attempting to retrieve account from database.
        try:
            # TODO this is prob not good but it works!
            self.__override_database_connection_with_self() #model.database_connection.initialize(self.sqlite_connection)
            account_model = model.Account.get(model.Account.username==username)
        except Exception as _:
            pass
        
        # If account is found create interface!
        if account_model is not None:
            return interface.AccountInterface(
                account_model=account_model
            )
        else:
            return account_model
    
    # TODO look for a better method, this is prob not safe :?
    def __override_database_connection_with_self(self):
        model.database_connection.initialize(self.sqlite_connection)
