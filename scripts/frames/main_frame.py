import tkinter as tk
from tables import Bank
from frames.frame_setting import FrameSet


class MainFrame(tk.Frame):
    def __init__(self, master, table, parent_id=None, parent_frame=None):
        super().__init__(master)
        self.master = master
        self.table = table
        self.parent_id = parent_id
        self.parent_frame=parent_frame   

        frame_set = FrameSet(root=self.master, parent=self.parent_frame, table=self.table)
        frame_set.window_set(title=f"{self.table.cls_name} Menu", width=330, height=250)
        if not isinstance (self.table, Bank):
            frame_set.back_set()
        
        self.label = tk.Label(self.master, text=f"Enter <{self.table.pk}> for search:")
        self.entry = tk.Entry(self.master)
        self.details_button = tk.Button(self.master, text="Search", command=self.details)
        self.create_button = tk.Button(self.master, text=f"Create {self.table.cls_name}", command=self.create)
        self.read_button = tk.Button(self.master, text=f"{self.table.cls_name} List", command=self.read)

        self.label.place(x=10, y=50, width=200, height=30)
        self.entry.place(x=10, y=90, width=200, height=30)
        self.details_button.place(x=10, y=130, width=100, height=30)
        self.create_button.place(x=170, y=170, width=150, height=30)
        self.read_button.place(x=170, y=210, width=150, height=30)


    def get_rows(self):
        if self.parent_id:
            search_fk = {self.table.fk: self.parent_id}
            return self.table.rows(**search_fk)
        
        return self.table.rows()


    def read(self):
        from frames.read_frame import ReadFrame

        self.rows = self.get_rows()

        if self.rows:
            read_frame = tk.Toplevel(self.master)
            ReadFrame(read_frame, self.table, self.rows, self.master)
            self.master.withdraw()
        else:
            tk.messagebox.showinfo(f"{self.table.cls_name}", "Not found")


    def details(self):
        from frames.details_frame import DetailsFrame

        search_pk = {self.table.pk: self.entry.get()}
        row = self.table.row(**search_pk)
        
        if row:
            if row.get(self.table.fk) == self.parent_id:
                details_frame = tk.Toplevel(self.master)
                DetailsFrame(details_frame, self.table, row, self.master)
                self.master.withdraw()
            else:
                tk.messagebox.showinfo(f"{self.table.cls_name}", "Access denied")
        else:
            tk.messagebox.showinfo(f"{self.table.cls_name}", "Not found")


    def create(self):
        from frames.create_frame import CreateFrame

        create_frame = tk.Toplevel(self.master)
        CreateFrame(create_frame, self.table, self.parent_id, self.master)
        self.master.withdraw()
