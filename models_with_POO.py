from abc import ABC, abstractmethod
from datetime import datetime


class Client:
    def __init__(self, adress):
        self._adress = adress
        self._accounts = []

    @property
    def address(self):
        return self._address
    
    @property
    def accounts(self):
        return self._accounts

    def add_account(self, account):
        self._accounts.append(account)

    def carry_out_transaction(self, transaction, account):
        transactions_today = account.history.today_transactions()
        if len(transactions_today) >= account.daily_transactions_limit:
            print("@@@ Transaction limit for the day exceeded! @@@")
            return
        transaction.register(account)


class NaturalPerson(Client):
    def __init__(self, name, birth_date, cpf, address):
        super().__init__(address)
        self.name = name
        self.birth_date = birth_date
        self.cpf = cpf

    
class Account:
    def __init__(self, client, number):
        self._balance = 0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = History()

    @property
    def balance(self):
        return self._balance
    
    @property
    def number(self):
        return self._number
    
    @property
    def agency(self):
        return self._agency
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history
    
    @classmethod
    def new_account(cls, client, number):
        return cls(client, number)
        
    def withdraw(self, amount):
        # Sacar dinheiro
        balance = self.balance
        exceeded_balance = amount > balance

        if exceeded_balance:
            print("@@@ Operation failed! Insufficient funds. @@@")
        elif amount > 0:
            self._balance -= amount
            print("$$$ Withdrawal successful! $$$")
            return True
        else:
            print("@@@ Operation failed! The amount must be positive. @@@")
        return False

    def deposit(self, amount):
        # Depositar dinheiro
        if amount > 0:
            self._balance += amount
            print("$$$ Deposit successful! $$$")
            return True
        else:
            print("@@@ Operation failed! The amount must be positive. @@@")
            return False


class CurrentAccount(Account):
    def __init__(self, client, number, limit=500, withdraw_limit=3, daily_transactions_limit=10):
        super().__init__(client, number)
        self._limit = limit
        self._withdraw_limit = withdraw_limit
        self._daily_transactions_limit = daily_transactions_limit

    @property
    def limit(self):
        return self._limit
  
    @property
    def withdraw_limit(self):
        return self._withdraw_limit
    
    @property
    def daily_transactions_limit(self):
        return self._daily_transactions_limit
    
    def withdraw(self, amount):
        # Sacar dinheiro
        number_withdrawals_today = sum(1 for details in self.history.transactions if details["type"] == "Withdrawal" and details["date"].startswith(datetime.now().strftime("%d/%m/%Y")))
        print(number_withdrawals_today)
        
        exceeded_limit = amount > self.limit
        exceeded_withdraw_limit = number_withdrawals_today >= self.withdraw_limit

        if exceeded_limit:
            print("@@@ Operation failed! Amount greater than the withdrawal limit. @@@")
        elif exceeded_withdraw_limit:
            print("@@@ Operation failed! The transaction exceeds the daily withdrawal amount @@@")
        else:
            return super().withdraw(amount)
        return False

    def __str__(self):
        return f"Agency: {self.agency} | Current Account: {self.number} | Client: {self.client.name}"


class History:
    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append({"type": transaction.__class__.__name__, "value": transaction.value, "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")})

    def generate_report(self, type_transaction=None):
        header = "\n================ EXTRATO ================"
        extract = ""
        transactions = self.transactions
        if not transactions:
            yield header
            yield "Não foram realizadas movimentações."
            return

        if type_transaction == "D":
            header = "\n================ EXTRATO - DEPÓSITO ================"
            yield header
            deposits = [op for op in transactions if op["type"] == "Deposit"]
            if not deposits:
                extract = "Não foram realizadas movimentações de depósito."
                yield extract
                return
            
            for op in deposits:
                extract = f"\n{op['date']}\nOperação: Depósito\nValor:\tR$ {op['value']:.2f}\n"
                yield extract
        elif type_transaction == "S":
            header = "\n================ EXTRATO - SAQUE ================"
            yield header
            withdrawals = [op for op in transactions if op["type"] == "Withdrawal"]
            if not withdrawals:
                extract = "Não foram realizadas movimentações de saque."
                yield extract
                return
            for op in withdrawals:
                extract = f"\n{op['date']}\nOperação: Saque\nValor:\tR$ {op['value']:.2f}\n"
                yield extract
        else:
            yield header
            for op in transactions:
                type_op = 'Depósito' if op['type'] == 'Deposit' else 'Saque'
                extract = f"\n{op['date']}\nOperação: {type_op}\nValor:\tR$ {op['value']:.2f}\n"
                yield extract
    
    def today_transactions(self):
        today = datetime.now().strftime("%d/%m/%Y")
        return [t for t in self.transactions if t["date"].startswith(today)]
        
    
class Transaction(ABC):
    """ Classe abstrata, vai garantir o contrato para as classe que à herdem. """
    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def value(self):
        return self._amount
    
    def register(self, account):
        sucess_transaction = account.deposit(self.value)
        if sucess_transaction:
            account.history.add_transaction(self)


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def value(self):
        return self._amount
    
    def register(self, account):
        sucess_transaction = account.withdraw(self.value)
        if sucess_transaction:
            account.history.add_transaction(self)