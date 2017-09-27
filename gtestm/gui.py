#!/usr/bin/env python3
import platform
import tkinter as tk
from tkinter import ttk

from gtestm.gui import gui_util as gu
from gtestm.run import request as req

OS = platform.system()


class CoreFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        # Generate all gui components
        self.service = req.Backend()
        self.refresh_button = ttk.Button(self, command=CoreFrame.refresh)
        self.test_display = gu.ScrollCanvas(self)
        self.data_label = ttk.Label(self, text="")
        self.state_label = ttk.Label(self, text="Hello")
        self.state_bar = ttk.Progressbar(self)
        self.progress_double = tk.DoubleVar(self)
        # Configure the widgets
        self._config_widgets()
        # Layout the widgets
        self._layout_widgets()

        self.bind("<<ReqData>>", self.launch_dialog)
        self.bind("<<Refresh>>", self.refresh)
        self.bind("<<Updated>>", self.fetch_new)
        self.bind("<<EndUpdate>>", self.restore_completion)

    def _config_widgets(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)
        self.refresh_button.config(text="Refresh", command=self.refresh)
        self.state_bar.configure(variable=self.progress_double)

    def _layout_widgets(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.test_display.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.E + tk.S + tk.W)
        self.state_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)
        self.data_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)
        self.refresh_button.grid(row=0, column=1, sticky=tk.E + tk.W)

    def initialize(self):
        self.test_display.update()
        self.test_display.event_generate("<<Configure>>")

    def launch_dialog(self, event):
        another = tk.Toplevel(self, bd=0, height=50, width=600, highlightthickness=0, takefocus=True)
        another.transient(self)
        another.protocol("WM_DELETE_WINDOW", lambda: self.fail_cred_check(another))
        gu.LoginFrame(another, self.service)
        another.grab_set()
        another.mainloop()
        another.wait_window(another)

    def fail_cred_check(self, window):
        self.restore_completion()
        window.destroy()

    def restore_completion(self, event=None):
        self.refresh_button.grid(row=0, column=1, sticky=tk.E + tk.W)
        self.state_bar.grid_forget()
        t = self.service.get_tests()
        self.test_display.wrapped_frame.give_data(t)
        self.data_label.configure(text=str(self.service.testdata))

    def fetch_new(self, event=None):
        print("Max:", req.quant, "\nStuff", req.progress)
        self.state_label.configure(text=str(req.progress) + "/" + str(req.quant))
        self.state_bar.configure(maximum=req.quant)
        self.progress_double.set(req.progress)

    def refresh(self, event=None):
        self.state_bar.grid(row=0, column=1, sticky=tk.N + tk.E + tk.S + tk.W)
        self.refresh_button.grid_forget()
        self.service.do_full_refresh(self)
        self.state_bar.configure(maximum=1)
        self.progress_double.set(0)


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.title("CSGeist")
    frame = CoreFrame(root)
    root.after(1, frame.initialize)
    root.mainloop()
