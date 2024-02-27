from database import model, interface, secure


# TODO include email method to retrieve an account.
def get_account(username: str) -> interface.AccountInterface | None:
    """Retrieve an account using the username.

    Args:
        username (str): Target username to find the account by.

    Returns:
        interface.AccountInterface | None: Returns AccountInterface if successful.
    """
    account_model: model.Account | None = None

    try:
        # TODO include use for model.change_database_to later after I make my planned changes.
        account_model = model.Account.get(
            username==username
        )
    except Exception as _:
        pass

    if account_model:
        return interface.AccountInterface(
            account_model=account_model
        )
    
    return None


def create_account(username: str, password: str) -> interface.AccountInterface | None:
    pass