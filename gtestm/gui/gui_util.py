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

        self.wrapped_frame = SortableTable(self.internal_frame, ["hi", "hi2"], [str.__gt__, str.__gt__])
        self.wrapped_frame.give_data([("first", "first2"), ("second", "second2")])

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
            height=max(cd[1], self.internal_frame_max_height),
            width=max(cd[0], self.internal_frame_max_width)
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

    def give_data(self, data):
        for datum in data:
            for panel, member in zip(self.category_panels, datum):
                label = ttk.Label(panel, text=str(member))
                label.pack(fill=tk.X)

    def unsort(self):
        for button in self.category_buttons:
            button.unset_dir()

    def sort(self, direction, category):
        pass


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

    def call_sort(self):
        self.table.unsort()
        if self.sort_dir is None:
            self.sort_dir = 0
        if self.sort_dir == 0:
            self.sort_dir = 1
        if self.sort_dir == 1:
            self.sort_dir = 0
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
        # Configure the widgets
        self._config_widgets()
        # Layout the widgets
        self._layout_widgets()

    def _config_widgets(self):
        self.extern_frame_sty.configure('Extern.TFrame', background='red')
        self.intern_frame_sty.configure('Intern.TFrame', background='blue')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.configure(style="Extern.TFrame")
        self.test_display.configure(style="Intern.TFrame")
        self.refresh_button.config(text="Refresh", command=self.refresh)

    def _layout_widgets(self):
        self.pack(fill=tk.BOTH, expand=True)
        self.test_display.grid(row=0, column=0, sticky=tk.N + tk.E + tk.S + tk.W)
        self.refresh_button.grid(row=1, column=0, sticky=tk.E + tk.W)

    def initialize(self):
        print("configure")
        self.test_display.update()
        self.test_display.event_generate("<<Configure>>")

    def refresh(self):
        print("Hi.")


if __name__ == "__main__":
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    frame = CoreFrame(root)
    root.after(1, frame.initialize)
    root.mainloop()
