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
        self.menubar = tk.Menu(self)
        self.configoptions = tk.Menu(self.menubar, tearoff=0)

        self.test_display = gu.ScrollCanvas(self)
        self.test_table = gu.SortableTable(self.test_display.internal_frame, ["test", "status"], [str.__gt__, str.__gt__])
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
        self.menubar.add_cascade(label="Configuration", menu=self.configoptions)
        self.configoptions.add_command(label="Set options", command=self.launch_settings_dialog)
        self.master.config(menu=self.menubar)

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
        self.test_table.pack(expand=True, fill=tk.BOTH)

    def _bind_events(self):
        self.bind("<<ReqData>>", self.launch_dialog)
        self.bind("<<Refresh>>", self.start_refresh)
        self.bind("<<Updated>>", self.next_refresh)
        self.bind("<<StartSetUp>>", self.set_starting)
        self.bind("<<StartFetch>>", self.set_fetching)
        self.bind("<<StartRun>>", self.set_running)
        self.bind("<<EndUpdateWrongDir>>", self.spec_reset)
        self.bind("<<EndUpdate>>", self.finish_refresh)
        self.bind("<<EndUpdate-FAIL>>", self.fail_refresh)

    def initialize(self):
        self.test_display.update()
        self.test_display.event_generate("<<Configure>>")

    def launch_settings_dialog(self):
        if self.dia is None:
            another = tk.Toplevel(self, bd=0, height=50, width=600, highlightthickness=0, takefocus=True)
            self.dia = another
            another.transient(self)
            another.protocol("WM_DELETE_WINDOW", lambda: self.fail_cred_check(another))
            gu.SettingsFrame(another)
            another.grab_set()
            another.wait_window(another)
            another.mainloop()

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
        self.test_table.lock_selection(True)
        sel = self.test_table.fetch_selected("test")
        if sel:
            self.service.do_refresh(self, hashlist=sel)
        else:
            self.service.do_refresh(self)

    def next_refresh(self, event=None):
        self.state_label.configure(text="{}/{}".format(self.service.statedata.progress, self.service.statedata.quant))
        self.state_bar.configure(maximum=self.service.statedata.quant)
        self.state_bar.configure(value=self.service.statedata.progress)
        self.dia = None

    def finish_refresh(self, event=None):
        self.refresh_button.grid(row=0, column=1, sticky=tk.E + tk.W)
        self.state_bar.grid_forget()
        t = self.service.get_tests()
        self.test_table.give_data(t, False if self.test_table.fetch_selected("test") else True, "test")
        self.test_table.lock_selection(False)
        self.data_label.configure(text=str(self.service.testdata))

    def fail_refresh(self, event=None):
        self.test_table.lock_selection(False)
        self.refresh_button.grid(row=0, column=1, sticky=tk.E + tk.W)
        self.data_label.configure(text="Failed.")

    def spec_reset(self, event=None):
        self.test_table.lock_selection(False)
        self.finish_refresh()
        self.data_label.configure(text="Failed to locate directory or wrong test directory was provided")


if __name__ == "__main__":
    print("Please launch main.py, instead, with the following command: main.py -m gui_utils")
