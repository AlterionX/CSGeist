import tkinter as tk
from tkinter import ttk


count = 0


def mouse_wheel(event):
    global count
    # respond to Linux or Windows wheel event
    if event.num == 5 or event.delta == -120:
        count -= 1
    if event.num == 4 or event.delta == 120:
        count += 1


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.master.title("G Test Manager")

        self.ut_id = ttk.Label(master, text="CS ID:")
        self.password = ttk.Label(master, text="Password:")

        vcmd_1 = master.register(self.validate_ut_id)  # we have to wrap the command
        self.ut_id_ = ttk.Entry(master, validate="key", validatecommand=(vcmd_1, '%P'))
        vcmd_2 = master.register(self.validate_password)  # we have to wrap the command
        self.password_ = ttk.Entry(master, show="*", validate="key", validatecommand=(vcmd_2, '%P'))

        self.sign_in = ttk.Button(master, text="Sign In", command=lambda: self.update("sign_in"))
        self.quit = ttk.Button(master, text="Quit", command=lambda: self.update("quit"))

        self.render_layout()

    def render_layout(self):
        self.ut_id.grid(row=0, column=0, sticky=tk.W)
        self.ut_id_.grid(row=0, column=1, columnspan=2, sticky=tk.E)

        self.password.grid(row=1, column=0, sticky=tk.W)
        self.password_.grid(row=1, column=1, columnspan=2, sticky=tk.E)

        self.sign_in.grid(row=2, column=0)
        self.quit.grid(row=2, column=1)

    def validate_ut_id(self, new_text):
        if not len(new_text.strip()):
            return False
        self.UTID = new_text
        return True

    def validate_password(self, new_text):
        if not len(new_text.strip()):
            return False
        self.PSSWD = new_text
        return True

    def update(self, method):
        if method == "sign_in":
            if len(self.UTID) > 0 and len(self.PSSWD) > 0:
                set_profile(self.UTID, self.PSSWD)
                self.master.quit()
        elif method == "quit":
            self.master.master.destroy()


if __name__ == "__main__":
    print("please run gui_util.py")
