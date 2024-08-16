import mysql.connector
from tkinter import messagebox
from functools import wraps


def catch_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        conn = self.__dict__.get("conn")
        try:
            return func(self, *args, **kwargs)

        except mysql.connector.Error as err:
            conn.rollback()
            messagebox.showerror(
                "Error",
                f"Failed to search {self.cls_name}: {err}"
            )
    return wrapper
