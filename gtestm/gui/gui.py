import tkinter as tk
from tkinter import ttk

def set_profile(id, psd):
    print ("ID: " + id + "   " + "PSD: " + psd)

def is_logged_in():
    return True

def do_full_refresh():
    print ("Full Refresh Requested")

def get_tests():
    hash_ = {}
    for element in range(100):
        status = "PASS"
        if element % 2 == 0:
            if element % 4 == 0:
                status = "COMPILE ERR"
            else:
                status = "FAIL"
        if element % 7 == 0:
            status = "INVALID"

        hash_["test_Test_test" + str(element)] = status
    return hash_


class Overview(tk.Frame):
    def __init__(self, root):

        tk.Frame.__init__(self, root)
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.master = self.frame

        self.tests_widgets = []

        if not is_logged_in():
            log_in = LoginFrame(tk.Toplevel())
            log_in.mainloop()
            log_in.master.withdraw()

        self.refresh = ttk.Button(self.master, text="Refresh", command=lambda: self.update("refresh"))

        self.render_layout()

    def render_layout(self):

        self.refresh.grid(row=0, column=2, sticky=tk.W)

        self.render_tests()

    def render_tests(self):

        self.foreground = {"PASS" : "white", "FAIL" : "white", "INVALID" : "white", "COMPILE ERR" : "white"}
        self.background = {"PASS" : "green", "FAIL" : "red", "INVALID" : "blue", "COMPILE ERR" : "blue"}

        # get rid of all the current tests
        for test in self.tests_widgets:
            test.grid_forget()

        tests_ = get_tests()
        passing_tests = filter(lambda x: tests_[x] == "PASS", tests_.keys())
        failing_tests = filter(lambda x: tests_[x] == "FAIL", tests_.keys())
        invalid_tests = filter(lambda x: tests_[x] == "INVALID", tests_.keys())
        comperr_tests = filter(lambda x: tests_[x] == "COMPILE ERR", tests_.keys())

        self.render_test_index = 0

        # tests are displayed in this order on the screen
        for test_hash in passing_tests:
            self.render_test(test_hash, tests_[test_hash])

        for test_hash in failing_tests:
            self.render_test(test_hash, tests_[test_hash])

        for test_hash in invalid_tests:
            self.render_test(test_hash, tests_[test_hash])

        for test_hash in comperr_tests:
            self.render_test(test_hash, tests_[test_hash])

    def render_test(self, test_hash, test_status):
        print ("called")
        self.render_test_index += 1

        test_hash_label = ttk.Label(self.master, text=test_hash)
        test_status_label = ttk.Label(self.master, text=test_status)

        test_status_label.configure(foreground=self.foreground[test_status])
        test_status_label.configure(background=self.background[test_status])

        test_hash_label.grid(row=self.render_test_index, column=0, columnspan=3, sticky=tk.W)
        test_status_label.grid(row=self.render_test_index, column=4, sticky=tk.E)

        self.tests_widgets.append(test_hash_label)
        self.tests_widgets.append(test_status_label)
        return 0

    def update(self, method):

        if method == "refresh":
            do_full_refresh()

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class LoginFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.master = master

        aster.title("G Test Manager")

        self.ut_id = ttk.Label(master, text="CS ID:")
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

if __name__ == "__main__":
    root = tk.Tk()
    Overview(root)
    root.mainloop()