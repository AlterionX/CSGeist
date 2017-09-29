#!/usr/bin/env python3
import platform
import tkinter as tk
from argparse import Namespace
from tkinter import ttk

from gtestm.gui_utils import gui_util as gu
from gtestm.run import request as req
from gtestm.netcfg import config
from gtestm.utils import testdata

OS = platform.system()


def main(args: Namespace, cfg: config.Config):
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.title("CSGeist")
    frame = CoreFrame(req.Backend(testdata.StateData(), testdata.TestData(), cfg), root)
    root.after(1, frame.initialize)
    root.mainloop()


class CoreFrame(ttk.Frame):
    def __init__(self, service, master=None):
        super().__init__(master=master)
        self.service = service

        # Generate all gui components
        self.test_display = gu.ScrollCanvas(self)
        self.dia = None

        self.state_label = ttk.Label(self, text="Hello")
        self.state_bar = ttk.Progressbar(self)
        self.refresh_button = ttk.Button(self, command=self.start_refresh)
        self.data_label = ttk.Label(self, text="")

        # Configure, layout the widgets, then bind the actions
        self._config_widgets()
        # Layout the widgets
        self._layout_widgets()
        self._bind_events()

    def _config_widgets(self):
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=27)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(1, weight=1)
        self.refresh_button.config(text="Refresh", command=self.start_refresh)

    def _layout_widgets(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.test_display.grid(row=1, column=0, columnspan=3, sticky=tk.N + tk.E + tk.S + tk.W)
        self.state_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)
        self.data_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)
        self.refresh_button.grid(row=0, column=1, sticky=tk.E + tk.W)

    def _bind_events(self):
        self.bind("<<ReqData>>", self.launch_dialog)
        self.bind("<<Refresh>>", self.start_refresh)
        self.bind("<<Updated>>", self.next_refresh)
        self.bind("<<StartSetUp>>", self.set_starting)
        self.bind("<<StartFetch>>", self.set_fetching)
        self.bind("<<StartRun>>", self.set_running)
        self.bind("<<EndUpdate>>", self.finish_refresh)

    def initialize(self):
        self.test_display.update()
        self.test_display.event_generate("<<Configure>>")

    def launch_dialog(self, event):
        if self.dia is None:
            another = tk.Toplevel(self, bd=0, height=50, width=600, highlightthickness=0, takefocus=True)
            self.dia = another
            another.transient(self)
            another.protocol("WM_DELETE_WINDOW", lambda: self.fail_cred_check(another))
            gu.LoginFrame(another, self.service)
            another.grab_set()
            another.wait_window(another)
            another.mainloop()

    def fail_cred_check(self, window):
        window.destroy()
        self.finish_refresh()

    def set_starting(self, event=None):
        self.data_label.configure(text=str("Setting up directory..."))

    def set_fetching(self, event=None):
        self.data_label.configure(text=str("Fetching list..."))

    def set_running(self, event=None):
        self.data_label.configure(text=str("Running..."))

    def start_refresh(self, event=None):
        self.state_bar.grid(row=0, column=1, ipadx=5, sticky=tk.N+tk.E+tk.S+tk.W)
        self.refresh_button.grid_forget()
        self.state_bar.configure(maximum=1)
        self.update()
        self.service.do_full_refresh(self)

    def next_refresh(self, event=None):
        print("Max:{}\nStuff:{}".format(self.service.statedata.quant, self.service.statedata.progress))
        self.state_label.configure(text="{}/{}".format(self.service.statedata.progress, self.service.statedata.quant))
        self.state_bar.configure(maximum=self.service.statedata.quant)
        self.state_bar.configure(value=self.service.statedata.progress)
        self.dia = None

    def finish_refresh(self, event=None):
        self.refresh_button.grid(row=0, column=1, sticky=tk.E + tk.W)
        self.state_bar.grid_forget()
        t = self.service.get_tests()
        self.test_display.wrapped_frame.give_data(t)
        self.data_label.configure(text=str(self.service.testdata))


if __name__ == "__main__":
    print("Please launch main.py, instead, with the following command: main.py -m gui_utils")
