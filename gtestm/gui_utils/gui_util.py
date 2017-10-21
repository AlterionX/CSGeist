import platform
import tkinter as tk
from tkinter import ttk

import time

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


class SettingsFrame:
    def __init__(self, master=None):
        pass


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
        self.categories = [""] + categories
        self.comp_fns = [None] + compare_fns

        self.check_label = ttk.Label(self)
        self.category_buttons = [ttk.Label(master=self, text="  ")] + [
            SortButton(self, master=self, category=str(category))
            for category in categories
        ]

        self.last_select = None

        self.dataitempairs = []

        self._config_widgets()
        self._layout_widgets()

    def _config_widgets(self):
        pass  # Nothing to configure...

    def _layout_widgets(self):
        for button, column in zip(self.category_buttons, range(len(self.categories))):
            if button is not None:
                button.grid(row=0, column=column, sticky=tk.E + tk.W + tk.N + tk.S)

    def give_data(self, data_dirt):
        if len(data_dirt) > len(self.dataitempairs):
            for _ in range(len(data_dirt) - len(self.dataitempairs)):
                self.dataitempairs.append([None, SortItem(self, categories=self.categories), None])
        else:
            for idx in range(len(self.dataitempairs) - len(data_dirt) + 1):
                self.dataitempairs[-idx][0] = None
                self.dataitempairs[-idx][1].check_state.set(0)
                self.dataitempairs[-idx][2] = None
        for key_v, idx in zip(data_dirt, range(len(data_dirt))):
            self.dataitempairs[idx][0] = (key_v, data_dirt[key_v]["status"])
            self.dataitempairs[idx][2] = data_dirt[key_v]
            self.dataitempairs[idx][1].set_data(self.dataitempairs[idx][0])
        self._avail_display()

    def _avail_display(self):
        for idx in range(len(self.dataitempairs)):
            datum, sortitem, _ = self.dataitempairs[idx]
            sortitem.clear()
            if datum is not None:
                sortitem.place(row=idx + 1)

        # Generate a configure event
        self.update()  # update table
        self.master.update()  # update frame holding table
        self.master.master.update()  # update canvas holding table
        self.master.master.master.event_generate("<<Configure>>")  # update frame containing scroll logic

    def unsort(self):
        for button in self.category_buttons[1:]:
            button.unset_dir()

    def sort(self, direction, category):
        if self.dataitempairs:
            self.dataitempairs = sorted(
                filter(lambda data: data[0] is not None, self.dataitempairs),
                key=lambda data: data[0][self.categories.index(category) - 1],
                reverse=(direction == 1)
            )
        self._avail_display()

    def fetch_selected(self, category):
        data = []
        for ds in self.dataitempairs:
            if ds[1].is_sel():
                data.append(ds[0][self.categories.index(category) - 1])
        return data

    def group_select(self, end):
        if self.last_select is not None:
            for idx in range(self.last_select, end - 1):
                self.dataitempairs[idx][1].check_state.set((self.dataitempairs[idx][1].check_state.get() + 1) % 2)
        self.last_select = end


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


class SortItem:
    COLORS = {
        "Status.PASS": ["white", "green"],
        "Status.FAIL": ["white", "red"],
        "Status.TOUT": ["white", "blue"],
        "Status.CERR": ["white", "black"]
    }
    _last_press = 0

    def __init__(self, table, categories=None):
        self.table = table
        self.check_state = tk.IntVar()
        self.check = ttk.Checkbutton(master=table)
        self.check.bind("<Button-1>", self._set_select)
        self.check.bind("<Shift-Button-1>", self._group_select)
        self.check.configure(variable=self.check_state, onvalue=1, offvalue=0)

        self.categories = categories
        self.composition = [self.check] + [ttk.Label(master=table) for _ in self.categories[1:]]

        self.index = 0

    def _set_select(self, event=None):
        print("Selecting item #", self.index)
        self.table.last_select = self.index

    def _group_select(self, event=None):
        print("Grooup selecting item #", self.index)
        self.table.group_select(self.index)

    def place(self, row):
        self.index = row
        for i in range(len(self.composition)):
            self.composition[i].grid(row=row, column=i, sticky=tk.E + tk.W + tk.N + tk.S)

    def set_data(self, data):
        for datum, d_label in zip(data, self.composition[1:]):
            d_label.configure(text=datum)
        if "state" in self.categories:
            self.composition[self.categories.index("state")].configure(
                foreground=SortItem.COLORS[str(data[self.categories.index("state") - 1])][0],
                background=SortItem.COLORS[str(data[self.categories.index("state") - 1])][1]
            )

    def clear(self):
        for widget in self.composition:
            widget.grid_forget()

    def is_sel(self):
        return self.check_state.get()

    def fetch_attr(self, ind):
        return self.composition[ind]
