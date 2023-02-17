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
        relief=RIDGE,  # FIXME: Remove/change default for relief
    ):
        frm = Frame(master=window, width=width, height=height, relief=relief)

        frm.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky="nsew",
        )

        self._frm = frm

    # FIXME: Make show and hide abstract methods? Would the map etc really be a subwindow then?


class MainMenu(SubWindow):
    def __init__(self, window, banner_text, menu_options):
        """Create a frame inside of `window` that fills up its entire row and
        column span"""
        super().__init__(window, None, None, 0, 0, *window.grid_size())

        # Add banner message
        lbl = Label(
            master=self._frm,
            text=banner_text,
            justify=CENTER,
            anchor=CENTER,
            style=STYLES["main_menu"]["style"],
        )

        lbl.pack(fill=BOTH)

        # Add text menu with desired options
        self.__text_menu = TextMenu(
            options=menu_options,
            master=self._frm,
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
        self._frm.grid_remove()

    def show(self):
        self._frm.grid()

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
            master=self._frm,
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
        self._frm.children["!label"].configure(text=text)


class EventLog(SubWindow):
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
            self._frm, num_lines, padx, pady
        )

    def write(self, message):
        event_log_text_box = self.__textbox

        # Make text box writable for a brief instant, write to it, then make it
        # read-only again
        event_log_text_box.config(state=NORMAL)
        event_log_text_box.insert(END, message + "\n")
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
    # FIXME: Remove/change default for relief
    def __init__(self, window, width, relief=RIDGE):
        self._frm = Frame(
            master=window,
            relief=relief,
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


class Inventory:
    def __init__(self, window, title, title_ipady, padx, pady, item_labels):
        self.__window = window
        self.__padx = padx
        self.__pady = pady
        self.__item_labels = item_labels

        # Create label for inventory
        lbl_inventory = Label(
            master=self.__window,
            text=title,
            relief=RIDGE,
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


class SideBar(SubWindow):
    def __init__(
        self,
        window,
        width,
        height,
        row,
        column,
        rowspan,
        columnspan,
        padx,
        pady,
        hp_gauge_height,
        hp_gauge_bar_width,
        hp_gauge_label_padx,
        hp_gauge_bar_padx,
        hp_gauge_bar_pady,
        inventory_title_ipady,
        inventory_padx,
        inventory_pady,
        inventory_item_labels,
    ):
        super().__init__(
            window, width, height, row, column, rowspan, columnspan
        )
        self.__padx = padx
        self.__pady = pady
        self.__hp_gauge_height = hp_gauge_height
        self.__hp_gauge_bar_width = hp_gauge_bar_width
        self.__hp_gauge_label_padx = hp_gauge_label_padx
        self.__hp_gauge_bar_padx = hp_gauge_bar_padx
        self.__hp_gauge_bar_pady = hp_gauge_bar_pady
        self.__inventory_title_ipady = inventory_title_ipady
        self.__inventory_padx = inventory_padx
        self.__inventory_pady = inventory_pady
        self.__inventory_item_labels = inventory_item_labels

        # Create hp gauge
        self.hp_gauge = self.__create_hp_gauge()

        self.inventory = self.__create_inventory()

    def __create_inventory(self):
        return Inventory(
            self._frm,
            title="Inventory",
            title_ipady=self.__inventory_title_ipady,
            padx=self.__inventory_padx,
            pady=self.__inventory_pady,
            item_labels=self.__inventory_item_labels,
        )

    def __create_hp_gauge(
        self,
    ):
        # Create frame to hold hp gauge label and bar
        frm_hp = Frame(master=self._frm, height=self.__hp_gauge_height)
        frm_hp.pack(
            side=TOP,
            padx=self.__padx,
            pady=self.__pady,
        )

        lbl_hp_gauge = Label(
            master=frm_hp, text="HP", style=STYLES["hp_gauge_label"]["style"]
        )
        lbl_hp_gauge.pack(padx=(self.__hp_gauge_label_padx, 0), side=LEFT)

        # Create bar for hp gauge
        bar_hp_gauge = Progressbar(
            master=frm_hp,
            orient=HORIZONTAL,
            length=self.__hp_gauge_bar_width,
            mode="determinate",
        )
        bar_hp_gauge.pack(
            padx=self.__hp_gauge_bar_padx, pady=self.__hp_gauge_bar_pady
        )

        # Initialize to full health
        bar_hp_gauge["value"] = 100

        return bar_hp_gauge


class InGameMenu(PopUpWindow):
    """
    A pop-up window with a text-based menu inside.
    """

    # FIXME: Remove/change default for relief
    def __init__(self, window, width, title, pady, menu_options, relief=RIDGE):
        # Create the frame for the whole in-game menu
        super().__init__(window, width, relief)

        # Create header with title in it
        frm_title = Frame(master=self._frm, width=width, relief=relief)
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

    def __init__(self, window, width, text, pady, dismiss_key, relief=RIDGE):
        # Create the frame for the whole in-game menu
        super().__init__(window, width, relief)

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
