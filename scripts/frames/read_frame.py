import tkinter as tk
from frames.frame_setting import FrameSet


class ReadFrame(tk.Frame):
    def __init__(self, master, table, rows, parent_frame):
        super().__init__(master)
        self.master = master
        self.table = table
        self.rows = rows
        self.parent_frame = parent_frame

        frame_set = FrameSet(root=self.master, parent=self.parent_frame, table=self.table)
        frame_set.window_set(title=f"Show all {self.table.cls_name}")
        frame_set.back_set()

        rows_str = "\n\n".join(["\n".join([f"{k}: {v}" for k, v in r.items()]) for r in rows])

        self.txt = tk.Text(self.master)
        self.txt.place(x=10, y=50, width=380, height=340)
        self.txt.insert("end", rows_str)
