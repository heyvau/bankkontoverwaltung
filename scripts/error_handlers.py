import mysql.connector
from tkinter import messagebox
from functools import wraps


def catch_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error",
                f"Failed to search {self.cls_name}: {err}"
            )
    return wrapper
