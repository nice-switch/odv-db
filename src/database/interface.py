from database import model

class AccountInterface():
    def __init__(self, account_model: model.Account, new_account: bool | None = False):
        self.account_model: model.Account = account_model
        self.new_account: bool = new_account

    