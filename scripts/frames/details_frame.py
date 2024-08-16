import tkinter as tk
from decimal import Decimal
from frames.frame_setting import FrameSet


class DetailsFrame(tk.Frame):
    def __init__(self, master, table, row, parent_frame):
        super().__init__(master)
        self.master = master
        self.table = table
        self.row = row
        self.parent_frame = parent_frame

        frame_set = FrameSet(root=self.master, parent=self.parent_frame, table=self.table)
        frame_set.window_set(title=f"{self.table.cls_name} Details", height=420)
        frame_set.back_set()

        self.txt = tk.Text(self.master)
        self.txt.place(x=10, y=50, width=380, height=150)
        row_str = "\n".join([f"{k}: {v}" for k, v in row.items()])
        self.txt.insert("end", row_str)
        self.button = tk.Button(self.master, text=f"Delete {self.table.cls_name}", command=self.delete)
        self.button.place(x=10, y=210, width=150, height=30)

        self.optional_widgets()


    def optional_widgets(self):
        from tables import SaveAccount, CurrentAccount

        y = 300
        if isinstance(self.table, (SaveAccount, CurrentAccount)):
            buttons = [
                tk.Button(self.master, text="Deposit", command=self.deposit),
                tk.Button(self.master, text="Withdraw", command=self.withdraw)
            ]
            self.deposit_entry = tk.Entry(self.master)
            self.withdraw_entry = tk.Entry(self.master)
            entries = [self.deposit_entry, self.withdraw_entry]

            for (b, e) in zip(buttons, entries):
                b.place(x=10, y=y, width=100, height=30)
                e.place(x=120, y=y, width=60, height=30)
                y += 40

            if isinstance(self.table, SaveAccount):
                interest_button = tk.Button(self.master, text="Calculate Interest", command=self.calculate_interest)
                interest_button.place(x=10, y=380, width=150, height=30)
        else:
            for ref in self.table.references:
                self.button = tk.Button(
                    self.master, text=f"{ref.cls_name} Menu",
                    command=lambda table=ref: self.to_menu(table)
                )
                self.button.place(x=10, y=y, width=150, height=30)
                y += 40


    def delete(self):
        search_pk = {self.table.pk: self.row.get(self.table.pk)}
        self.table.delete(**search_pk)
        self.master.destroy()
        self.parent_frame.deiconify()


    def to_menu(self, table):
        from frames.main_frame import MainFrame

        self.main_frame = tk.Toplevel(self.master)
        MainFrame(self.main_frame, table, parent_id=self.row.get(self.table.pk), parent_frame=self.master)
        self.master.withdraw()

    
    def deposit(self):
        amount = Decimal(self.deposit_entry.get())
        self.table.deposit(iban=self.row.get("iban"), amount=amount)
        self.refresh()
        

    def withdraw(self):
        amount = Decimal(self.withdraw_entry.get())
        success = self.table.withdraw(iban=self.row.get("iban"), amount=amount)
        if not success:
            tk.messagebox.showinfo(f"{self.table.cls_name} Withdraw", "There are not enough funds on your balance.")
        else:
            self.refresh()

    def calculate_interest(self):
        self.table.calculate_interest(iban=self.row.get("iban"))
        self.refresh()


    def refresh(self):
        search_pk = {self.table.pk: self.row.get(self.table.pk)}
        row = self.table.row(**search_pk)

        details_frame = tk.Toplevel(self.parent_frame)
        DetailsFrame(details_frame, self.table, row, self.parent_frame)
        self.master.destroy()
        
