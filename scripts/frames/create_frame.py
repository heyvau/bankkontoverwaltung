import tkinter as tk
from frames.frame_setting import FrameSet


class CreateFrame(tk.Frame):
    def __init__(self, master, table, parent_id, parent_frame):
        super().__init__(master)
        self.master = master
        self.table = table
        self.parent_id = parent_id
        self.parent_frame = parent_frame

        frame_set = FrameSet(root=self.master, parent=self.parent_frame, table=self.table)
        frame_set.window_set(title=f"Create {self.table.cls_name}", width=330, height=250)
        frame_set.back_set()

        self.labels = [tk.Label(self.master, text=field.replace("_", " "), anchor='w') for field in self.table.fields]
        self.entries = [tk.Entry(self.master) for field in self.table.fields]

        y = 50
        for (l, e) in zip(self.labels, self.entries):
            l.place(x=10, y=y, width=110, height=30)
            e.place(x=120, y=y, width=200, height=30)
            y += 40

        self.button = tk.Button(self.master, text=f"New {self.table.cls_name}", command=self.create)
        self.button.place(x=10, y=y+30, width=150, height=30)


    def create(self):
        data = {
            field: entry.get()
            for field, entry
            in zip(self.table.fields, self.entries)
        }
        if self.parent_id:
            data[self.table.fk] = self.parent_id

        self.table.insert(**data)
        self.master.destroy()
        self.parent_frame.deiconify()
