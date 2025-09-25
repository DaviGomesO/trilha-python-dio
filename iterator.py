class AccountIterator:
    def __init__(self, accounts):
        self._accounts = accounts
        self._index = 0
        pass

    @property
    def accounts(self):
        return self._accounts

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    def __iter__(self):
        return self

    def __next__(self):
        try:
            account = self.accounts[self.index]
            return f"\
              \nAgência:\t{account.agency}\
              \nNúmero:\t\t{account.number:04d}\
              \nTitular:\t{account.client.name}\
              \nSaldo:\t\tR$ {account.balance:.2f}\n\
            "
        except IndexError:
            raise StopIteration
        finally:
            self.index += 1
