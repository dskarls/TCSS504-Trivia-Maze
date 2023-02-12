import functools
from tkinter import *
from tkinter.ttk import *


class TextTriviaMazeView:
    """A text-based view for the Trivia Maze application that uses tkinter
    (specifically, themed-tkinter aka "ttk"). Currently, the size is fixed upon
    creation.
    """

    __MAP_WIDTH = 800
    __MAP_HEIGHT = 500
    __SIDEBAR_WIDTH = 250
    __HP_GAUGE_HEIGHT = 30
    __HP_GAUGE_BAR_WIDTH = int(0.8 * __SIDEBAR_WIDTH)
    __EVENT_LOG_HEIGHT = 50
    __EVENT_LOG_NUM_LINES = 10

    def __init__(self, title, theme_path=None, theme_name=None):
        self.__subwindows = {}

        # Create primary tkinter window and bind mainloop method (might fit
        # better in the driver and we can just pass the main Tk window into the
        # view init?
        self.__window = Tk()
        self.__window.title(title)
        self.mainloop = self.__window.mainloop

        if theme_path and theme_name:
            # To use this theme, clone the relevant repo and then give the path to its
            # azure.tcl file here
            self.__window.tk.call("source", theme_path)
            self.__window.tk.call("set_theme", theme_name)

        # Set minimum row/col sizes to prevent frames from collapsing to their
        # contained content
        self.__window.rowconfigure(0, minsize=self.__MAP_HEIGHT)
        self.__window.columnconfigure(0, minsize=self.__MAP_WIDTH)
        self.__window.columnconfigure(1, minsize=self.__SIDEBAR_WIDTH)

        # Set up the initial component frames
        self.__map = self.__add_map()
        self.__hp_gauge, self.__inventory = self.__add_hp_gauge_and_inventory()
        self.__event_log = self.__add_event_log()

        # Prevent resizing
        self.__window.resizable(False, False)

        # Capture keystrokes so they can be sent to the controller for
        # interpretation
        self.__window.bind(
            "<KeyPress>", self.__forward_keystroke_to_controller
        )
        # Also capture arrow keys
        self.__window.bind(
            "<Left>",
            self.__forward_keystroke_to_controller,
        )

    def __forward_keystroke_to_controller(self, event):
        # For regular keys
        key = event.char

        # If char was empty, check to see if it was an arrow key
        if not key:
            key = event.keysym

        if key:
            # If keysym wasn't empty, forward it to controller. Otherwise, just
            # ignore it since it's not a supported key command.

            # FIXME: This should really be sent to the controller. Just writing to
            # the event log here for demonstration purposes.
            self.write_to_event_log(f"You pressed {key}")

    def __add_subwindow(
        self, width, height, row, column, rowspan=1, columnspan=1
    ):
        frm = Frame(
            master=self.__window, width=width, height=height, relief=RIDGE
        )

        frm.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky="nsew",
        )

        return frm

    def __update_text_in_subwindow(
        self, subwindow_name, text_content, justify=CENTER
    ):
        frm = self.__subwindows[subwindow_name]

        # Update frame widget so we can get its width
        frm.update()
        frm_width = frm.winfo_width()

        lbl = Label(
            master=frm,
            text=text_content,
            wraplength=frm_width,
            justify=justify,
        )
        lbl.pack(
            fill=BOTH,
            padx=3,
            pady=3,
        )

    @staticmethod
    def __add_scrollable_readonly_textbox_to_subwindow(subwindow, num_lines):
        frm = subwindow
        scrlbar = Scrollbar(master=frm, orient=VERTICAL)
        scrlbar.pack(side=RIGHT, pady=5, fill=Y, padx=3)

        scrltxt = Text(
            master=frm,
            height=num_lines,
            yscrollcommand=scrlbar.set,
        )
        scrltxt.pack(fill=BOTH, pady=2)

        # Enable dragging of scroll bar now that text box exists (has to be
        # done in this order)
        scrlbar.config(command=scrltxt.yview)

        # Make text box read-only
        scrltxt.config(state=DISABLED)

    def __add_map(self):
        return self.__add_subwindow(self.__MAP_WIDTH, self.__MAP_HEIGHT, 0, 0)

    def __add_hp_gauge_and_inventory(self):
        # Create vertical sidebar frame
        frm_sidebar = self.__add_subwindow(
            width=self.__SIDEBAR_WIDTH,
            height=self.__MAP_HEIGHT,
            row=0,
            column=1,
        )

        # Create frame to hold hp gauge label and bar
        hp_gauge_padx = 15
        frm_hp = Frame(master=frm_sidebar, height=self.__HP_GAUGE_HEIGHT)
        frm_hp.grid(
            row=0, column=0, padx=hp_gauge_padx, pady=15, sticky="nsew"
        )

        # Create label for hp gauge
        lbl_hp_gauge = Label(master=frm_hp, text="HP ")
        lbl_hp_gauge.pack(side=LEFT)

        # Create bar for hp gauge
        bar_hp_gauge = Progressbar(
            master=frm_hp,
            orient=HORIZONTAL,
            length=self.__HP_GAUGE_BAR_WIDTH,
            mode="determinate",
        )
        bar_hp_gauge.pack(side=LEFT)
        bar_hp_gauge["value"] = 100

        # Create label for inventory
        lbl_inventory = Label(
            master=frm_sidebar,
            text="Inventory",
            relief=RIDGE,
            anchor=CENTER,
        )
        lbl_inventory.grid(sticky="nsew", pady=(5, 10))

        inventory_quantity_labels = self.__create_inventory_item_labels(
            frm_sidebar, hp_gauge_padx
        )

        return bar_hp_gauge, inventory_quantity_labels

    @staticmethod
    def __create_inventory_item_labels(frm, padx):
        # Create inventory_labels
        item_labels = (
            "Health Potion",
            "Suggestion Potion",
            "Vision Potion",
            "Magic Key",
            "Pillar of Abstraction",
            "Pillar of Encapsulation",
            "Pillar of Inheritance",
            "Pillar of Polymorphism",
        )
        inventory_quantity_labels = {}
        for item in item_labels:
            # Create frame for this item
            frm_item = Frame(master=frm)
            frm_item.grid(sticky="nsew", padx=padx, pady=10)

            # Create label for item
            lbl_item = Label(master=frm_item, text=item)
            lbl_item.pack(side=LEFT, padx=padx)

            # Create label holding quantity of item
            lbl_quantity = Label(master=frm_item, text="0")
            lbl_quantity.pack(side=RIGHT, padx=padx)

            inventory_quantity_labels[item] = lbl_quantity

        return inventory_quantity_labels

    def __add_event_log(self):
        # event_log_name = "event log"
        frm = self.__add_subwindow(
            None, self.__EVENT_LOG_HEIGHT, 1, 0, columnspan=2
        )
        self.__add_scrollable_readonly_textbox_to_subwindow(
            frm, self.__EVENT_LOG_NUM_LINES
        )
        return frm

    def write_to_event_log(self, message):
        event_log_text_box = self.__event_log.children["!text"]

        # Make text box writable for a brief instant, write to it, then make it
        # read-only again
        event_log_text_box.config(state=NORMAL)
        event_log_text_box.insert(END, message + "\n")
        event_log_text_box.config(state=DISABLED)

        # Scroll down as far as possible
        event_log_text_box.yview(END)


if __name__ == "__main__":
    view = TextTriviaMazeView("TriviaMaze")

    for i in range(100):
        view.write_to_event_log(f"Here is message {i}")
    view.mainloop()
