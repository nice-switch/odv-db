from database import model

class AccountInterface():
    def __init__(self, account_model: model.Account):
        self.account_model: model.Account = account_model

    def get_username(self) -> str:
        return self.account_model.username
    
    def get_hashed_password(self) -> str:
        return self.account_model.get("password")
    
    def get_salt(self) -> str:
        return self.account_model.get("salt")

    def get_blob(self) -> str:
        return self.account_model.get("blob")


    