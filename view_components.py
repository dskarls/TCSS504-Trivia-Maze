import functools

from tkinter import *
from tkinter.ttk import *


from view_config import STYLES


class TextMenu:
    """A menu of strings traversable with arrow keys. The selected element can
    be colored differently from the rest of the elements. Intended to be used
    with keystroke detection to make a selection."""

    def __init__(
        self,
        options,
        master,
        width,
        height,
        unselected_foreground_color,
        unselected_background_color,
        selected_foreground_color,
        selected_background_color,
        font,
        justify,
    ):
        self.__options = options
        self.__list_box = Listbox(
            master,
            width=width,
            height=height,
            font=font,
            foreground=unselected_foreground_color,
            background=unselected_background_color,
            selectforeground=selected_foreground_color,
            selectbackground=selected_background_color,
            justify=justify,
        )
        self.__add_options()

        # Pack into containing frame
        self.__list_box.pack()

        # Set first element as selected
        self.__list_box.select_set(0)

    def focus(self):
        """Have this widget take focus"""
        self.__list_box.focus()

    def __add_options(self):
        for ind, option in enumerate(self.__options):
            self.__list_box.insert(ind + 1, option)

    @property
    def selected_option(self):
        return self.__options[self.__list_box.curselection()[0]]

    @selected_option.setter
    def selected_option(self, index):
        self.__list_box.select_set(index)


class SubWindow:
    def __init__(
        self,
        window,
        width,
        height,
        row,
        column,
        rowspan=1,
        columnspan=1,
    ):
        frm = Frame(master=window, width=width, height=height)

        frm.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky="nsew",
        )

        # Expose tk frame so that this object can be passed to other interface
        # objects, e.g. HP Gauge, as a master
        self.frame = frm

    # FIXME: Make show and hide abstract methods? Would the map etc really be a subwindow then?


class MainMenu(SubWindow):
    def __init__(self, window, banner_text, menu_options):
        """Create a frame inside of `window` that fills up its entire row and
        column span"""
        super().__init__(window, None, None, 0, 0, *window.grid_size())

        # Add banner message
        lbl = Label(
            master=self.frame,
            text=banner_text,
            justify=CENTER,
            anchor=CENTER,
            style=STYLES["main_menu"]["style"],
        )

        lbl.pack(fill=BOTH)

        # Add text menu with desired options
        self.__text_menu = TextMenu(
            options=menu_options,
            master=self.frame,
            width=None,
            height=len(menu_options),
            unselected_foreground_color="grey",
            unselected_background_color="black",
            selected_foreground_color="black",
            selected_background_color="white",
            font=("Courier New", 18),
            justify=CENTER,
        )

    def hide(self):
        self.frame.grid_remove()

    def show(self):
        self.frame.grid()

        # Attach focus to text menu of options
        self.__text_menu.focus()
        self.__text_menu.selected_option = 0

    @property
    def selected_option(self):
        return self.__text_menu.selected_option

    @selected_option.setter
    def selected_option(self, index):
        self.__text_menu.selected_option = index


class Map(SubWindow):
    def __init__(self, window, width, height, row, column, padx, text):
        super().__init__(
            window,
            width,
            height,
            row,
            column,
        )
        self.__text = text

        # Create empty label that will hold the actual map
        lbl = Label(
            master=self.frame,
            text=text,
            style=STYLES["map"]["style"],
            justify=CENTER,
            anchor=CENTER,
        )
        lbl.pack(padx=padx, fill=BOTH)

    @property
    def contents(self):
        return self.__text

    @contents.setter
    def contents(self, text):
        self.frame.children["!label"].configure(text=text)


class EventLog(SubWindow):
    __PREFIX = "> "

    def __init__(
        self,
        window,
        width,
        num_lines,
        row,
        column,
        rowspan,
        columnspan,
        padx,
        pady,
    ):
        super().__init__(window, width, None, row, column, rowspan, columnspan)

        self.__textbox = self.__add_scrollable_readonly_textbox_to_subwindow(
            self.frame, num_lines, padx, pady
        )

    def write(self, message):
        event_log_text_box = self.__textbox

        # Make text box writable for a brief instant, write to it, then make it
        # read-only again
        event_log_text_box.config(state=NORMAL)
        event_log_text_box.insert(END, self.__PREFIX + message + "\n")
        event_log_text_box.config(state=DISABLED)

        # Scroll down as far as possible
        event_log_text_box.yview(END)

    @staticmethod
    def __add_scrollable_readonly_textbox_to_subwindow(
        subwindow, num_lines, padx, pady
    ):
        frm = subwindow
        scrlbar = Scrollbar(master=frm, orient=VERTICAL)
        scrlbar.pack(side=RIGHT, pady=pady, fill=Y, padx=padx)

        scrltxt = Text(
            master=frm,
            height=num_lines,
            yscrollcommand=scrlbar.set,
        )
        scrltxt.pack(fill=BOTH, pady=pady)

        # Enable dragging of scroll bar now that text box exists (has to be
        # done in this order)
        scrlbar.config(command=scrltxt.yview)

        # Make text box read-only
        scrltxt.config(state=DISABLED)

        return scrltxt


class PopUpWindow:
    def __init__(self, window, width):
        self._frm = Frame(
            master=window,
        )
        self._place_pop_up_at_center_of_window(self._frm, width)
        self._width = width

    @staticmethod
    def _place_pop_up_at_center_of_window(frame, width):
        frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER,
            width=width,
        )

    # FIXME: Make show and hide abstract methods? Would the map etc really be a subwindow then?


class EnumeratedInventory:
    def __init__(self, window, title, title_ipady, padx, pady, item_labels):
        self.__window = window
        self.__padx = padx
        self.__pady = pady
        self.__item_labels = item_labels

        # Create label for inventory
        lbl_inventory = Label(
            master=self.__window,
            text=title,
            anchor=CENTER,
            style=STYLES["inventory_title"]["style"],
        )
        lbl_inventory.pack(
            side=TOP,
            ipady=title_ipady,
            fill=BOTH,
        )

        self.__create_inventory_item_labels()

    def __create_inventory_item_labels(self):
        inventory_quantity_labels = {}

        for item in self.__item_labels:
            # Create frame for this item
            frm_item = Frame(master=self.__window)
            frm_item.pack(
                side=TOP, fill=BOTH, padx=self.__padx, pady=self.__pady
            )

            # Create label for item
            lbl_item = Label(
                master=frm_item,
                text=item,
                style=STYLES["inventory_item"]["style"],
            )
            lbl_item.pack(side=LEFT, padx=self.__padx)

            # Create label holding quantity of item
            lbl_quantity = Label(
                master=frm_item,
                text="0",
                style=STYLES["inventory_item"]["style"],
            )
            lbl_quantity.pack(side=RIGHT, padx=self.__padx)

            inventory_quantity_labels[item] = lbl_quantity

        return inventory_quantity_labels


class CheckboxInventory:
    def __init__(self, window, title, title_ipady, padx, pady, item_labels):
        self.__window = window
        self.__padx = padx
        self.__pady = pady
        self.__item_labels = item_labels

        # Create label for inventory
        lbl_inventory = Label(
            master=self.__window,
            text=title,
            anchor=CENTER,
            style=STYLES["pillars_title"]["style"],
        )
        lbl_inventory.pack(
            side=TOP,
            ipady=title_ipady,
            fill=BOTH,
        )

        self.__create_inventory_item_labels()

    def __create_inventory_item_labels(self):
        inventory_quantity_labels = {}

        control_vars = [IntVar() for _ in range(len(self.__item_labels))]

        for ind, item in enumerate(self.__item_labels):
            # Create frame for this item
            frm_item = Frame(master=self.__window, height=50)
            frm_item.pack(
                side=TOP, fill=BOTH, padx=self.__padx, pady=self.__pady
            )

            # Create label for item
            lbl_item = Label(
                master=frm_item,
                text=item,
                style=STYLES["pillars_item"]["style"],
            )
            lbl_item.pack(side=LEFT, padx=self.__padx)

            # Create checkbutton indicating if the item is held
            # NOTE: Using `partial` is necessary here to prevent all of the
            # command closures form just taking the final value of `ind` after
            # the loop is exhausted.
            check_btn = Checkbutton(
                frm_item,
                variable=control_vars[ind],
                onvalue=1,
                offvalue=0,
                command=functools.partial(
                    lambda ind: control_vars[ind].set(
                        1 - control_vars[ind].get()
                    ),
                    ind=ind,
                ),
            )
            check_btn.pack(side=RIGHT, padx=self.__padx)
            control_vars[ind].set(0)
            inventory_quantity_labels[item] = check_btn

        return inventory_quantity_labels


class HPGauge:
    def __init__(
        self,
        window,
        height,
        bar_width,
        label_padx,
        bar_padx,
        bar_pady,
    ):
        # Create frame to hold hp gauge label and bar
        frm = Frame(master=window, height=height)
        frm.pack(
            side=TOP,
        )

        lbl_hp_gauge = Label(
            master=frm, text="HP", style=STYLES["hp_gauge_label"]["style"]
        )
        lbl_hp_gauge.pack(padx=(label_padx, 0), side=LEFT)

        # Create bar for hp gauge
        self.__bar_hp_gauge = Progressbar(
            master=frm,
            orient=HORIZONTAL,
            length=bar_width,
            mode="determinate",
        )
        self.__bar_hp_gauge.pack(padx=bar_padx, pady=bar_pady)

        # Initialize to full health
        self.set(100)

    def set(self, value):
        self.__bar_hp_gauge["value"] = value


class InGameMenu(PopUpWindow):
    """
    A pop-up window with a text-based menu inside.
    """

    def __init__(self, window, width, title, pady, menu_options):
        # Create the frame for the whole in-game menu
        super().__init__(window, width)

        # Create header with title in it
        frm_title = Frame(master=self._frm, width=width)
        frm_title.pack(fill=BOTH, anchor=CENTER)
        lbl = Label(
            master=frm_title,
            text=title,
            justify=CENTER,
            anchor=CENTER,
        )
        lbl.pack(fill=BOTH, pady=pady)

        self.__text_menu = TextMenu(
            options=menu_options,
            master=self._frm,
            width=width,
            height=len(menu_options),
            unselected_foreground_color="grey",
            unselected_background_color="black",
            selected_foreground_color="black",
            selected_background_color="white",
            font=("Courier New", 18),
            justify=CENTER,
        )

    def show(self):
        self._place_pop_up_at_center_of_window(self._frm, self._width)
        self.__text_menu.focus()
        self.__text_menu.selected_option = 0

    def hide(self):
        self._frm.place_forget()

    @property
    def selected_option(self):
        return self.__text_menu.selected_option

    @selected_option.setter
    def selected_option(self, index):
        self.__text_menu.selected_option = index


class DismissiblePopUp(PopUpWindow):
    """
    A pop-up window that simply displays a message and allows the user to
    dismiss it by entering a specific key.
    """

    def __init__(self, window, width, text, pady, dismiss_key):
        # Create the frame for the whole in-game menu
        super().__init__(window, width)

        lbl = Label(
            master=self._frm,
            text=text,
            justify=CENTER,
            anchor=CENTER,
            style=STYLES["game_won_menu"]["style"],
        )
        lbl.pack(fill=BOTH, pady=pady)

        # Put return to main menu option below
        lbl = Label(
            master=self._frm,
            text=f"Press [{dismiss_key}] to return to main menu",
            justify=CENTER,
            anchor=CENTER,
        )
        lbl.pack(
            fill=BOTH,
        )

    def show(self):
        self._place_pop_up_at_center_of_window(self._frm, self._width)

    def hide(self):
        self._frm.place_forget()
