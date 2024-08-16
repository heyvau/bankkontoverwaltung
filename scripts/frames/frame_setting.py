import tkinter as tk


class FrameSet:
    def __init__(self, root, parent, table):
        self.root = root
        self.parent = parent
        self.table = table


    def window_set(self, title="", width=400, height=400):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width/2) - (width/2))
        y = int((screen_height/2) - (height/2))

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.title(title)


    def back_set(self):
        self.root.protocol("WM_DELETE_WINDOW", self.back)
        self.root.back_button = tk.Button(self.root, text="←", command=self.back)
        self.root.back_button.place(x=10, y=10, width=30, height=30)

        self.root.exit_button = tk.Button(self.root, text="EXIT", command=self.end)
        self.root.exit_button.place(x=50, y=10, width=60, height=30)


    def back(self):
        self.root.destroy()
        self.parent.deiconify()


    def end(self):
        self.table.conn.close()
        self.table.cursor.close()
        exit()
