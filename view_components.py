from abc import ABC, abstractmethod
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
            activestyle="none",
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
        """Add the options supplied during initialization to the list of
        options in the menu."""
        for ind, option in enumerate(self.__options):
            self.__list_box.insert(ind + 1, option)

    def reset_selection(self):
        """Unselects all lines and sets the first item as active"""
        self.__list_box.selection_clear(0, END)
        self.__list_box.activate(0)
        self.selected_option = 0

    @property
    def selected_option(self):
        """Used to expose which option in the menu the user has selected."""
        return self.__options[self.__list_box.curselection()[0]]

    @selected_option.setter
    def selected_option(self, index):
        """Used to set which option in the menu the user has selected."""
        self.__list_box.selection_set(index)
        self.__list_box.activate(index)


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
        """A wrapper around tk.Frame to represent a subsection of the
        application master frame, specified via its grid, wherein widgets can
        be inserted."""
        frm = Frame(master=window, width=width, height=height)

        frm.grid(
            row=row,
            column=column,
            rowspan=rowspan,
            columnspan=columnspan,
            sticky=NSEW,
        )

        # Expose tk frame so that this object can be passed to other interface
        # objects, e.g. HP Gauge, as a master
        self.frame = frm


class MainMenu(SubWindow):
    """The main menu widget that is displayed before the player begins the
    game. Contains a banner message and an arrow-scrollable text menu."""

    def __init__(self, window, banner_text, menu_options):
        """Create a frame inside of the frame specified by `window` that fills
        up its entire row and column span."""
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
        """Hide this widget."""
        self.frame.grid_remove()

    def show(self):
        """Show this widget."""
        self.frame.grid()

        # Attach focus to text menu of options
        self.__text_menu.focus()
        self.__text_menu.reset_selection()
        self.frame.update_idletasks()

    @property
    def selected_option(self):
        """Used to expose which option in the menu the user has selected."""
        return self.__text_menu.selected_option

    @selected_option.setter
    def selected_option(self, index):
        """Used to set which option in the menu the user has selected."""
        self.__text_menu.selected_option = index


class Map(SubWindow):
    """The map that shows the maze to the player."""

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
        lbl.pack(padx=padx, fill=BOTH, expand=True)

    @property
    def contents(self):
        """Used to expose the text string underlying the maze map."""
        return self.__text

    @contents.setter
    def contents(self, text):
        """Used to set the text string underlying the maze map."""
        self.__text = text
        self.frame.children["!label"].configure(text=text)


class EventLog(SubWindow):
    """
    The text box that logs notable events for the player to see.
    """

    # String prefixed to all log entries
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

        # Initialize a var to track whether the log has already been written
        # to. This is used to determine prefixes/postfixes wrapped around each
        # message.
        self.__contents_empty = True

    def write(self, message):
        """Write a message in a new line of the event log."""
        event_log_text_box = self.__textbox

        if self.__contents_empty:
            message_wrapped = ""
        else:
            message_wrapped = "\n"

        message_wrapped += self.__PREFIX + message

        # Make text box writable for a brief instant, write to it, then make it
        # read-only again
        event_log_text_box.config(state=NORMAL)
        event_log_text_box.insert(END, message_wrapped)
        event_log_text_box.config(state=DISABLED)

        # Scroll down as far as possible
        event_log_text_box.yview(END)

        self.__contents_empty = False

    @staticmethod
    def __add_scrollable_readonly_textbox_to_subwindow(
        subwindow, num_lines, padx, pady
    ):
        """Creates and embeds into the event log frame a read-only scrollable
        text box with scroll bar."""
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

    def clear(self):
        """Clear contents of the event log."""
        self.__textbox.config(state=NORMAL)
        self.__textbox.delete("1.0", END)
        self.__textbox.config(state=DISABLED)


class EnumeratedInventory:
    """An inventory of items that have an positive integer count value
    associated with them."""

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

        self.__item_quantity_labels = self.__create_inventory_item_labels()

    def __create_inventory_item_labels(self):
        """Create and pack the labels that hold the names of all of the items
        and their respective quantities."""
        item_quantity_labels = {}

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

            item_quantity_labels[item] = lbl_quantity

        return item_quantity_labels

    def update_item_quantity(self, item_name, quantity):
        """Set the quantity associated with an item based on its name."""
        self.__item_quantity_labels[item_name].configure(text=str(quantity))

    def clear(self):
        """Set all item quantities to zero."""
        for item_quantity_label in self.__item_quantity_labels.values():
            item_quantity_label.configure(text="0")


class CheckboxInventory:
    """An inventory of items that can either be held or not held, with
    checkboxes reflecting this state."""

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

        self.__item_check_button_control_vars = (
            self.__create_inventory_item_labels()
        )

    def __create_inventory_item_labels(self):
        """Create and pack the labels that hold the names of all of the items
        and their respective checkboxes."""
        item_check_button_control_vars = {}

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

            item_check_button_control_vars[item] = control_vars[ind]

            # Mark item as not held
            control_vars[ind].set(0)

        return item_check_button_control_vars

    def check_item(self, item_name):
        """Set an item as being held, checking its box."""
        self.__item_check_button_control_vars[item_name].set(1)

    def clear(self):
        """Set all items as not being held, unchecking their boxes."""
        for item_control_var in self.__item_check_button_control_vars.values():
            item_control_var.set(0)


class HPGauge:
    """A widget consisting of an 'HP' label and a bar indicating the value of
    the adventurer's hit points."""

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
        """Set the value of HP to reflect in the gauge."""
        self.__bar_hp_gauge["value"] = value


class PopUpWindow(ABC):
    """A pop-up window that does not belong to a frame's grid, but is rather
    displayed over the top of it."""

    def __init__(self, window, width):
        self._frm = Frame(
            master=window,
        )
        self._place_pop_up_at_center_of_window(self._frm, width)
        self._width = width

    @staticmethod
    def _place_pop_up_at_center_of_window(frame, width):
        """Position the pop-up window at the middle of the specified frame,
        occupying the specified width."""
        frame.place(
            relx=0.5,
            rely=0.5,
            anchor=CENTER,
            width=width,
        )

    @abstractmethod
    def show(self):
        """Show the pop-up window."""
        pass

    @abstractmethod
    def hide(self):
        """Hide the pop-up window."""
        pass


class InGameMenu(PopUpWindow):
    """
    A pop-up window with a text-based menu inside. To be accessed from the
    primary interface.
    """

    def __init__(self, window, width, title, padx, pady, menu_options):
        # Create the frame for the whole in-game menu
        super().__init__(window, width)

        # Create header with title in it
        frm_title = Frame(
            master=self._frm,
            width=width,
            relief=RIDGE,
        )
        frm_title.pack(fill=BOTH, anchor=CENTER)
        lbl = Label(
            master=frm_title,
            text=title,
            justify=CENTER,
            anchor=CENTER,
        )
        lbl.pack(fill=BOTH, padx=padx, pady=pady)

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
        """Show the in-game menu's window."""
        self._place_pop_up_at_center_of_window(self._frm, self._width)
        self.__text_menu.focus()
        self.__text_menu.reset_selection()
        self._frm.update_idletasks()

    def hide(self):
        """Hide the in-game menu's window."""
        self._frm.place_forget()

    @property
    def selected_option(self):
        """Used to expose which option in the menu the user has selected."""
        return self.__text_menu.selected_option

    @selected_option.setter
    def selected_option(self, index):
        """Used to set which option in the menu the user has selected."""
        self.__text_menu.selected_option = index


class DismissiblePopUp(PopUpWindow):
    """
    A pop-up window that simply displays a message and allows the user to
    dismiss it by entering a specific key.
    """

    def __init__(
        self,
        window,
        width,
        text,
        bottom_label,
        ipadx,
        ipady,
        text_style,
        bottom_label_style,
    ):
        # Create the frame for the whole in-game menu
        super().__init__(window, width)

        self.__lbl_primary = Label(
            master=self._frm,
            text=text,
            justify=CENTER,
            anchor=CENTER,
            style=text_style,
            relief=RIDGE,
        )
        self.__lbl_primary.pack(fill=BOTH, ipadx=ipadx, ipady=ipady)

        # Put return to main menu option below
        lbl = Label(
            master=self._frm,
            text=bottom_label,
            justify=CENTER,
            anchor=CENTER,
            style=bottom_label_style,
            relief=SUNKEN,
        )
        lbl.pack(fill=BOTH, ipadx=ipadx, ipady=ipady)

    def show(self):
        """Show the pop-up at the center of the parent frame."""
        self._place_pop_up_at_center_of_window(self._frm, self._width)
        self._frm.update_idletasks()

    def hide(self):
        """Hide the pop-up."""
        self._frm.place_forget()

    def set_text(self, text):
        """Set the underlying text content of the pop-up to the specified
        value."""
        self.__lbl_primary.configure(text=text)


class QuestionAndAnswerMenu(PopUpWindow):
    """
    An pop-up window with a question and answer prompt that displays a question
    and its options, and provides a way for the player to submit an answer.
    Should indicate to the user how to use a SuggestionPotion. Should also be
    capable of displaying a hint.
    """

    def __init__(self, window, width, title, pady):
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

        # Add an empty text section to hold the question itself
        self._question_lbl = Label(
            master=self._frm, text="", justify=CENTER, anchor=CENTER
        )
        self._question_lbl.pack(fill=BOTH, pady=pady)

        # TODO: Also display how many suggestion potions the user has
        # somewhere?

    def set_question(self, question_text):
        """
        Populates the question label with the specified text.

        Parameters
        ----------
        question_text : str
            String to fill in as question in the widget.
        """
        self._question_lbl.configure(text=question_text)

    @abstractmethod
    def set_hint(self, hint_text):
        """Sets the content of the hint text to the specified value.

        Parameters
        ----------
        hint_text : str
            The text to display as a hint in the widget.
        """
        pass

    @abstractmethod
    def get_user_answer(self):
        """Fetch and return the player's answer."""
        pass


class ShortAnswerQuestionAndAnswer(QuestionAndAnswerMenu):
    """A question and answer widget that the user can respond to with a
    free-form text answer."""

    def __init__(self, window, width, title, pady):
        super().__init__(window, width, title, pady)

        self.__user_input = Entry(master=self._frm, justify=CENTER)
        self.__user_input.pack(fill=BOTH, pady=pady)

        # Add an empty text section to hold a hint
        self.__hint_lbl = Label(
            master=self._frm, text="", justify=CENTER, anchor=CENTER
        )
        self.__hint_lbl.pack(fill=BOTH, pady=pady)

    def show(self):
        """Show the widget in the middle of the center of the parent frame and
        take focus."""
        self._place_pop_up_at_center_of_window(self._frm, self._width)
        self.__user_input.focus()
        self._frm.update_idletasks()

    def hide(self):
        """Hide the widget."""
        self._frm.place_forget()

    def get_user_answer(self):
        return self.__user_input.get()

    def set_options(self, text):
        return self.__options_lbl.configure(text=text)

    def set_hint(self, text):
        self.__hint_lbl.configure(text=text)
