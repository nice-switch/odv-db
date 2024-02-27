import json

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


def create_account(username: str, password: str, email: str | None = None) -> interface.AccountInterface | None:
    if not get_account(username):
        return None
    
    # hashes[0] is comparison hash
    # hashes[1] is the AES256 key for blob.
    hashes, salt = secure.hash_password(
        password=password.encode(),
        num_hashes=2
    )

    encrypted_data, nonce = secure.encrypt_data(
        password=hashes[1],
        data=b'["Hello", "World!"]'
    )

    new_account = model.Account.create(
        email = email or "",
        username=username,
        password=hashes[0].hex(),
        nonce=nonce.hex(),
        salt=salt.hex(),
        blob=encrypted_data.hex()
    )

    new_interface = interface.AccountInterface(
        account_model=new_account
    )

    return new_interface