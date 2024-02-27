from database import model


class AccountInterface():
    def __init__(self, account_model: model.Account):
        self.account_model: model.Account = account_model
        
