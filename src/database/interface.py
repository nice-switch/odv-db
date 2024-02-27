from database import model

# NOTE When making changes to the data of models, ensure model.change_database_to is used.
# God forbid I mix production and development data.

class AccountInterface():
    def __init__(self, account_model: model.Account):
        self.account_model: model.Account = account_model
        
