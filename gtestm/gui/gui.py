import tkinter as tk
from tkinter import ttk

def set_profile(id, psd):
    print ("ID: " + id + "   " + "PSD: " + psd)

def is_logged_in():
    return True

def do_full_refresh():
    print ("Full Refresh Requested")

def get_tests():
    return {"testasdasd": "PASS", "testasfasfasfsaf": "PASS", "testasfasfasdasdasdasdasdasfsafasf": "FAIL"}


class Overview(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        master.title("Overview")

        self.tests_widgets = []

        if not is_logged_in():
            log_in = LoginFrame(tk.Toplevel())
            log_in.mainloop()
            log_in.master.withdraw()

        self.refresh = ttk.Button(master, text="Refresh", command=lambda: self.update("refresh"))

        self.render_layout()

    def render_layout(self):

        self.refresh.grid(row=0, column=2, sticky=tk.W)

        self.render_tests()

    def render_tests(self):

        # get rid of all the current tests
        for test in self.tests_widgets:
            test.grid_forget()

        tests_ = get_tests()
        passing_tests = filter(lambda x: tests_[x] == "PASS", tests_.keys())
        failing_tests = filter(lambda x: tests_[x] == "FAIL", tests_.keys())

        index = 0
        for key in passing_tests:
            index += 1
            test_hash = ttk.Label(self.master, text=key)
            test_status = ttk.Label(self.master, text=tests_[key])

            test_status.winfo_rgb("green")

            test_hash.grid(row=index, column=0, columnspan=3, sticky=tk.W)
            test_status.grid(row=index, column=4, sticky=tk.E)

            self.tests_widgets.append(test_hash)
            self.tests_widgets.append(test_status)

        for key in failing_tests:
            index += 1
            test_hash = ttk.Label(self.master, text=key)
            test_status = ttk.Label(self.master, text=tests_[key])

            test_hash.grid(row=index, column=0, columnspan=3, sticky=tk.W)
            test_status.grid(row=index, column=4, sticky=tk.E)

            self.tests_widgets.append(test_hash)
            self.tests_widgets.append(test_status)

    def update(self, method):

        if method == "refresh":
            do_full_refresh()

class LoginFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # CONTENT
        self.master = master

        master.title("G Test Manager")

        self.ut_id = ttk.Label(master, text="UT ID:")
        self.password = ttk.Label(master, text="Password:")

        vcmd_1 = master.register(self.validate_ut_id) # we have to wrap the command
        self.ut_id_ = ttk.Entry(master, validate="key", validatecommand=(vcmd_1, '%P'))
        vcmd_2 = master.register(self.validate_password) # we have to wrap the command
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

root = tk.Tk()
overview = Overview(root)
overview.mainloop()