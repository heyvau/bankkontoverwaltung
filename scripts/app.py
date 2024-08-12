import tkinter as tk
from tables import Bank
from db_connection import get_db_connection


class BankApp(tk.Frame):
    def __init__(self, master, table):
        super().__init__(master)
        self.master = master
        self.table = table

        self.master.title("Bank Menu")
        self.master.geometry("300x150")
        self.search_label = tk.Label(self.master, text="Geben Sie BIC ein:")
        self.search_entry = tk.Entry(self.master)
        self.search_button = tk.Button(self.master, text="Search", command=self.show_details)
        self.insert_button = tk.Button(self.master, text="Add", command=self.add)
        self.rows_button = tk.Button(self.master, text="Show all", command=self.show_all)

        self.search_label.grid(row=0, columnspan=2, sticky="nwse", padx=10, pady=10)
        self.search_entry.grid(row=1, column = 0, sticky="nwse", padx=10, pady=10)
        self.search_button.grid(row=1, column = 1, sticky="nwse", padx=10, pady=10)
        self.insert_button.grid(row=2, column = 0, sticky="nwse", padx=10, pady=10)
        self.rows_button.grid(row=2, column = 1, sticky="nwse", padx=10, pady=10)

    
    def show_details(self):
        search_value = self.search_entry.get()
        row = self.table.row("bic", search_value)
        
        if row:
            row_str = "\n".join([f"{k}: {v}" for k, v in row.items()])
            show = tk.Toplevel(self.master)
            show.geometry("300x150")
            show.title(f"Show {self.table.cls_name}")
            txt = tk.Text(show, padx=10, pady=10)
            txt.pack()
            txt.insert("end", row_str)
            show.grab_set()
        else:
            tk.messagebox.showinfo(f"{self.table.cls_name}", "Not found")


    def add(self):
        pass


    def show_all(self):
        rows = self.table.rows()
        
        if rows:
            rows_str = "\n\n".join(["\n".join([f"{k}: {v}" for k, v in r.items()]) for r in rows])
            show = tk.Toplevel(self.master)
            show.geometry("400x300")
            show.title(f"Show all {self.table.cls_name}")
            txt = tk.Text(show, padx=10, pady=10)
            txt.pack()
            txt.insert("end", rows_str)
            show.grab_set()
        else:
            tk.messagebox.showinfo("Not found")


if __name__ == "__main__":
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    bank = Bank(conn, cursor)

    root = tk.Tk()
    BankApp(root, table=bank)

    root.mainloop()
    cursor.close()
    conn.close()
