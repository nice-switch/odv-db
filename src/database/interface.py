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
        hashes, _ = secure.hash_password(password, salt_override=bytes.fromhex(self.account_model.salt), num_hashes=2)

        authorization_password = hashes[0]

        if bytes.fromhex(self.account_model.password) == authorization_password:
            # TODO decrypt existing data and merge data

            new_hashes, salt = secure.hash_password(password, num_hashes=2)
            
            new_authorization_password = new_hashes[0]
            new_encryption_password = new_hashes[1]

            encrypted_data, nonce = secure.encrypt_data(
                new_encryption_password,
                json.dumps(data).encode()
            )

            self.account_model.password = new_authorization_password.hex()
            self.account_model.nonce = nonce.hex()
            self.account_model.salt = salt.hex()
            self.account_model.blob = encrypted_data.hex()

            self.account_model.save()

            return True
        
        return False


    

    def update_password(self, new_password: str, old_password: str | None = None) -> bool:
        decrypted_data = self.decrypt_data(old_password)

        if decrypted_data is not None:
    
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
            