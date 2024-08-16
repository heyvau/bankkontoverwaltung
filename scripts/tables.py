from base_table import BaseTable
from decimal import Decimal
from error_handlers import catch_error


class Bank(BaseTable):
    pass


class Customer(BaseTable):
    pass


class BaseAccount(BaseTable):
    @catch_error
    def insert(self, iban: str, balance: Decimal, customer_id: int, **kwargs: Decimal) -> None:
        """
        kwargs: 
        overdraft_limit=<value> for CurrentAccount
        interest_rate=<value> for SaveAccount
        """
        spec_field, spec_value = next(iter(kwargs.items()))
        self.cursor.execute(
            f'INSERT INTO Account (iban, balance, customer_id) \
            VALUES(%s, %s, %s)',
            (iban, balance, customer_id)
        )
        self.cursor.execute(
            f'INSERT INTO {self.cls_name} (account_id, {spec_field}) \
            VALUES(LAST_INSERT_ID(), %s)',
            (spec_value,)
        )
        self.conn.commit()


    @catch_error
    def rows(self, **kwargs) -> list[dict]:
        if not kwargs:
            self.cursor.execute(
                f'SELECT * FROM {self.cls_name} spec_a \
                INNER JOIN Account a \
                ON spec_a.account_id = a.account_id'
            )
        else:
            search_key, search_value = next(iter(kwargs.items()))
            self.cursor.execute(
                f'SELECT * FROM {self.cls_name} spec_a \
                INNER JOIN Account a \
                ON spec_a.account_id = a.account_id \
                WHERE a.{search_key} = %s',
                (search_value,)
            )
        return self.cursor.fetchall()


    @catch_error
    def row(self, **kwargs) -> dict | None:
        search_key, search_value = next(iter(kwargs.items()))
        self.cursor.execute(
            f'SELECT * FROM {self.cls_name} spec_a \
            INNER JOIN Account a \
            ON spec_a.account_id = a.account_id \
            WHERE a.{search_key} = %s',
            (search_value,)
        )
        return self.cursor.fetchone()

    
    @catch_error
    def delete(self, **kwargs) -> None:
        search_key, search_value = next(iter(kwargs.items()))
        self.cursor.execute(
            f'DELETE FROM Account \
            WHERE {search_key} = %s',
            (search_value,)
        )
        self.conn.commit()


    @catch_error
    def deposit(self, iban: str, amount: Decimal) -> None:
        self.cursor.execute(
            f'UPDATE Account \
            SET balance = balance + %s \
            WHERE iban = %s',
            (amount, iban)
        )
        self.conn.commit()


class SaveAccount(BaseAccount):
    @catch_error
    def withdraw(self, iban: str, amount: Decimal) -> bool:
        row = self.row(iban=iban)
        if not (row and row.get("balance") >= amount):
            return False

        self.cursor.execute(
            f'UPDATE Account \
            SET balance = balance - %s \
            WHERE iban = %s \
            AND balance >= %s',
            (amount, iban, amount)
        )
        self.conn.commit()
        return True
        

    @catch_error
    def calculate_interest(self, iban) -> None:
        self.cursor.execute(
            f'UPDATE Account AS a \
            INNER JOIN SaveAccount AS save_a \
            ON a.account_id = save_a.account_id \
            SET a.balance = a.balance * (1 + save_a.interest_rate * 0.01)  \
            WHERE a.iban = %s',
            (iban,)
        )
        self.conn.commit()


class CurrentAccount(BaseAccount):
    @catch_error
    def withdraw(self, iban, amount: Decimal) -> bool:
        row = self.row(iban=iban)
        if not (row and row.get("balance") + row.get("overdraft_limit") >= amount):
            return False

        self.cursor.execute(
            f'UPDATE Account AS a \
            INNER JOIN CurrentAccount AS curr_a \
            SET a.balance = a.balance - %s \
            WHERE a.iban = %s \
            AND a.balance + curr_a.overdraft_limit >= %s',
            (amount, iban, amount)
        )
        self.conn.commit()
        return True
