from database import model, secure


class BlobInterface():
    def __init__(self, encrypted_blob_data: str | None = None):
        self.encrypted_blob_data: bytes | None = bytes.fromhex(encrypted_blob_data)
        self.decrypted_blob_data: dict | None = None

    def decrypt_blob(self, password: str | bytes, salt: bytes, nonce: bytes, save_to_blob_interface: bool | None = False) -> bytes | None:
        if type(password) is str:
            password = password.encode()

        _, _, encryption_key = secure.hash_password(password, salt=salt)

        decrypted_data: bytes | None = secure.decrypt_data(
            data=self.encrypted_blob_data,
            key=encryption_key,
            nonce=nonce
        )

        if save_to_blob_interface:
            if decrypted_data is not None:
                self.decrypted_blob_data = decrypted_data

        return decrypted_data


class AccountInterface():
    def __init__(self, account_model: model.Account):
        self.account_model: model.Account = account_model

    def get_username(self) -> str:
        return self.account_model.username
    
    def get_password(self) -> str:
        return self.account_model.password
    
    def get_email(self) -> str:
        return self.account_model.email
    
    def get_nonce(self) -> str:
        return self.account_model.nonce

    def get_salt(self) -> str:
        return self.account_model.salt

    def get_blob(self) -> BlobInterface:
        return BlobInterface(self.account_model.blob)