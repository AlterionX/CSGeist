import platform
import tkinter as tk
from tkinter import ttk

OS = platform.system()


class DialogToplevel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.config(bd=0, height=50, width=600, highlightthickness=0, takefocus=True)
        self.transient(self)
        self.cancel_action = None
        self.success_action = None
        self.protocol("WM_DELETE_WINDOW", self.cancel_action)

    def set_internal(self, cancel=None, success=None, cancel_action=None, success_action=None):
        self.cancel_action = cancel_action
        self.success_action = success_action
        if cancel is not None:
            cancel.config(onclick=self.cancel)
        if success is not None:
            cancel.config(onclick=self.success)

    def cancel(self):
        if self.cancel_action is not None:
            self.cancel_action()
        self.destroy()

    def success(self):
        if self.success_action is not None:
            self.success_action()
        self.destroy()

    def begin(self):
        self.grab_set()
        self.mainloop()
        self.wait_window(self)


class LoginFrame(ttk.Frame):
    def __init__(self, master, service):
        super().__init__(master)

        self.master = master
        self.service = service

        self.master.title("G Test Manager")

        self.utid_var = tk.StringVar()
        self.utid_label = ttk.Label(master, text="CS ID:")
        self.utid_entry = ttk.Entry(master, textvariable=self.utid_var)
        self.psswd_var = tk.StringVar()
        self.psswd_label = ttk.Label(master, text="Password:")
        self.psswd_entry = ttk.Entry(master, show="*", textvariable=self.psswd_var)

        self.sign_in = ttk.Button(master, text="Sign In", command=self.update)

        self.render_layout()

        self.master.bind("<Return>", self.update)

    def render_layout(self):
        self.utid_label.grid(row=0, column=0, sticky=tk.W)
        self.utid_entry.grid(row=0, column=1, columnspan=2, sticky=tk.E)
        self.utid_entry.focus_force()

        self.psswd_label.grid(row=1, column=0, sticky=tk.W)
        self.psswd_entry.grid(row=1, column=1, columnspan=2, sticky=tk.E)

        self.sign_in.grid(row=2, column=1)

    def update(self, event=None):
        if len(self.utid_var.get()) > 0 and len(self.psswd_var.get()) > 0:
            self.master.destroy()
            self.service.set_profile(self.utid_var.get(), self.psswd_var.get())
            self.master.master.event_generate("<<Refresh>>")
            print("Here we are")


class ScrollCanvas(ttk.Frame):
    def __init__(self, master=None, maxh=300, maxw=300):
        super().__init__(master=master)
        self.internal_frame_max_height = maxh
        self.internal_frame_max_width = maxw
        self.canvas_base_sty = ttk.Style()
        self.canvas = tk.Canvas(self)

        self.internal_frame = ttk.Frame(self.canvas)
        self.internal_frame_id = self.canvas.create_window(
            5, 5,
            anchor=tk.N + tk.W,
            window=self.internal_frame
        )

        self.wrapped_frame = SortableTable(self.internal_frame, ["test", "state"], [str.__gt__, str.__gt__])

        self.vscroll = ttk.Scrollbar(self)
        self.hscroll = ttk.Scrollbar(self)

        self._config_widgets()
        self._layout_widgets()
        self._prep_scroll()
        self._set_boxdimen(None)
        self._bind_events()

    def on_vertical(self, event):
        if OS == 'Linux':
            if event.num == 4:
                self.canvas.yview_scroll((-1) * 2, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(2, "units")
        elif OS == 'Windows':
            self.canvas.yview_scroll((-1) * int((event.delta / 120) * 2), "units")
        elif OS == 'Darwin':
            self.canvas.yview_scroll(event.delta, "units")

    def on_horizontal(self, event):
        if OS == 'Linux':
            if event.num == 4:
                self.canvas.xview_scroll((-1) * 2, "units")
            elif event.num == 5:
                self.canvas.xview_scroll(2, "units")
        elif OS == 'Windows':
            self.canvas.xview_scroll((-1) * int((event.delta / 120) * 2), "units")
        elif OS == 'Darwin':
            self.canvas.xview_scroll(event.delta, "units")

    def _config_widgets(self):
        self.canvas_base_sty.configure("ScrollIntern.TFrame", background="green")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.canvas.configure(scrollregion=self.canvas.bbox(self.internal_frame_id))
        self.hscroll.configure(orient=tk.HORIZONTAL)

        self.internal_frame.configure(style="ScrollIntern.TFrame")

    def _prep_scroll(self):
        self.vscroll.config(command=self.canvas.yview)
        self.hscroll.config(command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)

    def _layout_widgets(self):
        self.vscroll.pack(fill=tk.Y, side=tk.RIGHT)
        self.hscroll.pack(fill=tk.X, side=tk.BOTTOM)
        self.canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.wrapped_frame.pack(expand=True, fill=tk.BOTH)

    def get_container(self):
        return self.internal_frame

    def _set_boxdimen(self, event=None):
        cd = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.internal_frame.configure(
            height=max(cd[1], max(self.internal_frame_max_height, self.internal_frame.winfo_reqheight())),
            width=max(cd[0], max(self.internal_frame_max_width, self.internal_frame.winfo_reqwidth()))
        )
        self.canvas.configure(scrollregion=self.canvas.bbox(self.internal_frame_id))

    def _bind_events(self):
        self.bind('<Visibility>', self._set_boxdimen)
        self.bind('<Configure>', self._set_boxdimen)
        self.bind('<<Configure>>', self._set_boxdimen)
        if OS == "Linux":
            self.master.master.bind("<Button-4>", self.on_vertical, add='+')
            self.master.master.bind("<Button-5>", self.on_vertical, add='+')
            self.master.master.bind("<Shift-Button-4>", self.on_horizontal, add='+')
            self.master.master.bind("<Shift-Button-5>", self.on_horizontal, add='+')
        else:
            self.master.master.bind('<MouseWheel>', self.on_vertical, add='+')
            self.master.master.bind('<Shift-MouseWheel>', self.on_horizontal, add='+')


class SortableTable(ttk.Frame):
    def __init__(self, master=None, categories=None, compare_fns=None):
        super().__init__(master)
        if categories is None:
            categories = []
        if compare_fns is None:
            compare_fns = []
        self.categories = categories
        self.comp_fns = compare_fns
        self.data = []

        self.category_panels = [ttk.Frame(self) for categories in categories]
        self.category_buttons = [
            SortButton(self, master=panel, category=str(category))
            for category, panel
            in zip(categories, self.category_panels)
        ]
        self.labels = [[] for _ in range(len(categories))]

        self._config_widgets()
        self._layout_widgets()

    def _config_widgets(self):
        for panel in self.category_panels:
            panel.configure(borderwidth=2, relief="groove")

    def _layout_widgets(self):
        for panel, button, column in zip(self.category_panels, self.category_buttons, range(len(self.category_panels))):
            # panel.pack(expand=True, fill=tk.Y, side=tk.LEFT)
            panel.grid(row=0, column=column, sticky=tk.E + tk.W + tk.N + tk.S)
            button.pack(side=tk.TOP, fill=tk.X)

    def give_data(self, data_dirt):
        self.data = None
        self.data = [(key_v, data_dirt[key_v]["status"]) for key_v in data_dirt]
        self._avail_display()

    def _avail_display(self):
        for cat_labels in self.labels:
            for label in cat_labels:
                label.pack_forget()
            cat_labels.clear()
        for datum in self.data:
            for panel, member, cat_labels in zip(self.category_panels, datum, self.labels):
                label = ttk.Label(panel, text=str(member))
                label.pack(fill=tk.X)
                cat_labels.append(label)
        colors = {
            "Status.PASS": ["white", "green"],
            "Status.FAIL": ["white", "red"],
            "Status.TOUT": ["white", "blue"],
            "Status.CERR": ["white", "black"]
        }
        for label in self.labels[self.categories.index("state")]:
            label.configure(foreground=colors[label.cget("text")][0], background=colors[label.cget("text")][1])
        # Generate a configure event
        self.configure(
            height=self.category_panels[0].winfo_height()
        )
        self.master.configure(
            height=self.category_panels[0].winfo_height()
        )
        self.master.event_generate("<Configure>")

    def unsort(self):
        for button in self.category_buttons:
            button.unset_dir()

    def sort(self, direction, category):
        if self.data:
            self.data = sorted(
                self.data,
                key=lambda data: data[self.categories.index(category)],
                reverse=(direction == 1)
            )
        self._avail_display()


class SortButton(ttk.Button):
    def __init__(self, table, master=None, category=None):
        super().__init__(master)
        self.table = table
        self.category = category
        self.configure(command=self.call_sort, text=self.category)
        self.unset_dir()
        self.sort_dir = None

    def unset_dir(self):
        self.sort_dir = None
        self.configure(text=self.category + "↕")

    def call_sort(self):
        save = self.sort_dir
        self.table.unsort()
        if save is None or save == 1:
            self.sort_dir = 0
            self.configure(text=self.category + "↓")
        if save == 0:
            self.sort_dir = 1
            self.configure(text=self.category + "↑")
        self.table.sort(direction=self.sort_dir, category=self.category)


if __name__ == "__main__":
    print("This platform is being transitioned. Please use gtestm.modes.gui_util instead.")
