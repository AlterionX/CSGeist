import tkinter as tk

def set_profile(id, psd):
    print "ID: " + id + "   " + "PSD: " + psd

class LoginFrame(tk.Frame):

    def __init__(self, master):
        
        # CONTENT

        self.master = master
        master.title("G Test Manager")

        self.ut_id = Label(master, text="UT ID:")
        self.password = Label(master, text="Password:")

        vcmd_1 = master.register(self.validate_ut_id) # we have to wrap the command
        self.ut_id_ = Entry(master, validate="key", validatecommand=(vcmd_1, '%P'))
        vcmd_2 = master.register(self.validate_password) # we have to wrap the command
        self.password_ = Entry(master, show="*", validate="key", validatecommand=(vcmd_2, '%P'))

        self.sign_in = Button(master, text="Sign In", command=lambda: self.update("sign_in"))
        self.quit = Button(master, text="Quit", command=master.quit)

        # LAYOUT

        self.ut_id.grid(row=0, column=0, sticky=W)
        self.ut_id_.grid(row=0, column=1, columnspan=2, sticky=E)

        self.password.grid(row=1, column=0, sticky=W)
        self.password_.grid(row=1, column=1, columnspan=2, sticky=E)

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

root = Tk()
log_in = LoginFrame(root)
log_in.mainloop()