#!/bin/usr/env python3
import tkinter as tk
from tkinter import ttk

import gtestm.modes.request as req


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
        self.canvas.yview_scroll(-1 * event.delta, 'units')

    def on_horizontal(self, event):
        self.canvas.xview_scroll(-1 * event.delta, 'units')

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

    def _set_boxdimen(self, event):
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

        self.bind('<MouseWheel>', self.on_vertical)
        self.bind("<Button-4>", self.on_vertical)
        self.bind("<Button-5>", self.on_vertical)

        self.bind('<Shift-MouseWheel>', self.on_horizontal)
        self.bind("<Shift-Button-4>", self.on_horizontal)
        self.bind("<Shift-Button-5>", self.on_horizontal)


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

        self.bind()
        self._config_widgets()
        self._layout_widgets()

    def _config_widgets(self):
        """self.rowconfigure(0, weight=1)
        for column in range(len(self.category_panels)):
            self.columnconfigure(column, weight=1)"""
        for panel in self.category_panels:
            panel.configure(borderwidth=2, relief="groove")

    def _layout_widgets(self):
        for panel, button, column in zip(self.category_panels, self.category_buttons, range(len(self.category_panels))):
            panel.pack(expand=True, fill=tk.Y, side=tk.LEFT)
            # panel.grid(row=0, column=column, sticky=tk.E + tk.W + tk.N + tk.S)
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
    # TODO arrows for sorting direction
    def __init__(self, table, master=None, category=None):
        super().__init__(master)
        self.table = table
        self.category = category
        self.configure(command=self.call_sort, text=self.category)
        self.sort_dir = None

    def unset_dir(self):
        self.sort_dir = None
        self.configure(text=self.category)

    def call_sort(self):
        save = self.sort_dir
        self.table.unsort()
        if save is None or save == 1:
            self.sort_dir = 0
            self.configure(text=self.category + "V")
        if save == 0:
            self.sort_dir = 1
            self.configure(text=self.category+"^")
        self.table.sort(direction=self.sort_dir, category=self.category)


class CoreFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        # Generate all gui components
        self.service = req.Backend()
        self.extern_frame_sty = ttk.Style()
        self.intern_frame_sty = ttk.Style()
        self.refresh_button = ttk.Button(self, command=CoreFrame.refresh)
        self.test_display = ScrollCanvas(self)
        self.state_bar = ttk.Progressbar(self)
        self.progress_double = tk.DoubleVar(self)
        # Configure the widgets
        self._config_widgets()
        # Layout the widgets
        self._layout_widgets()

        self.bind("<<Updated>>", self.fetch_new)
        self.bind("<<EndUpdate>>", self.restore_completion)

    def _config_widgets(self):
        self.extern_frame_sty.configure('Extern.TFrame', background='red')
        self.intern_frame_sty.configure('Intern.TFrame', background='blue')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.configure(style="Extern.TFrame")
        self.test_display.configure(style="Intern.TFrame")
        self.refresh_button.config(text="Refresh", command=self.refresh)
        self.state_bar.configure(variable=self.progress_double)

    def _layout_widgets(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.test_display.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.refresh_button.grid(row=1, column=0, sticky=tk.E + tk.W)

    def initialize(self):
        print("configure")
        self.test_display.update()
        self.test_display.event_generate("<<Configure>>")

    def restore_completion(self, event=None):
        self.state_bar.grid_forget()
        self.refresh_button.grid(row=1, column=0, sticky=tk.E + tk.W)
        t = self.service.get_tests()
        print(t)
        self.test_display.wrapped_frame.give_data(t)

    def fetch_new(self, event=None):
        print("Max:", req.quant, "\nStuff", req.progress)
        self.state_bar.configure(maximum=req.quant)
        self.progress_double.set(req.progress)

    def refresh(self, event=None):
        self.refresh_button.grid_forget()
        self.state_bar.grid(row=1, column=0, sticky=tk.E + tk.W)
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
