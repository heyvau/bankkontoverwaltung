import tkinter as tk
from tables import Bank, Customer, CurrentAccount, SaveAccount
from db_connection import get_db_connection
from frames.main_frame import MainFrame


if __name__ == "__main__":
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    save_account = SaveAccount(
        conn=conn, cursor=cursor,
        fields=("iban", "balance", "interest_rate"),
        pk="iban",
        fk="customer_id"
    )
    current_account = CurrentAccount(
        conn=conn, cursor=cursor,
        fields=("iban", "balance", "overdraft_limit"),
        pk="iban",
        fk="customer_id"
    )
    customer = Customer(
        conn=conn, cursor=cursor,
        fields=("name",),
        pk="customer_id",
        references=[save_account, current_account],
        fk = "bank_bic"
    )
    bank = Bank(
        conn=conn, cursor=cursor,
        fields=("bic", "name", "address"),
        pk="bic",
        references=[customer]
    )

    root = tk.Tk()
    MainFrame(root, table=bank)

    root.mainloop()
    cursor.close()
    conn.close()
