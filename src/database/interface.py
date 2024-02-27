import json

from database import model, secure

# NOTE When making changes to the data of models, ensure model.change_database_to is used.
# God forbid I mix production and development data.

class AccountInterface():
    def __init__(self, account_model: model.Account):
        self.account_model: model.Account = account_model
    

    def decrypt_data(self, password: str) -> dict | None:
        decrypted_data: dict | None = None

        try:
            aes_password = secure.hash_password(
                password=password.encode(),
                salt_override=bytes.fromhex(self.account_model.salt),
                num_hashes=2
            )[0][1]
            
            decrypted_data = json.loads(
                secure.decrypt_data(
                    aes_password,
                    bytes.fromhex(self.account_model.nonce),
                    bytes.fromhex(self.account_model.blob)
                )
            )
        except Exception as _:
            pass

        return decrypted_data


    def update_password(self, new_password: str, old_password: str | None = None, new_account: bool | None = False) -> bool:
        pass