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
            # TODO is this the cleanest it can be?...
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


    def update_data(self, password: str, data: dict) -> bool:
        pass
    

    def update_password(self, new_password: str, old_password: str | None = None) -> bool:
        decrypted_data = self.decrypt_data(old_password)

        if decrypted_data is not None:
            print("GO!")
            hashes, salt = secure.hash_password(new_password, num_hashes=2)

            authorization_key = hashes[0]
            encryption_key = hashes[1]
            
            encrypted_data, nonce = secure.encrypt_data(encryption_key, json.dumps(decrypted_data).encode())

            self.account_model.password = authorization_key.hex()
            self.account_model.salt = salt.hex()

            self.account_model.nonce = nonce.hex()
            self.account_model.blob = encrypted_data.hex()

            self.account_model.save()

            return True

        return False
            