from abc import abstractmethod

from trivia_maze_model_observer import TriviaMazeModelObserver


class TriviaMazeView(TriviaMazeModelObserver):
    """
    A view to display the trivia maze game to the user and gather input
    commands.
    """

    def __init__(self, maze_model, maze_controller):
        super().__init__(maze_model)
        self._maze_controller = maze_controller

    @abstractmethod
    def show_main_menu(self):
        """Display the main menu"""

    @abstractmethod
    def hide_main_menu(self):
        """Hide the main menu"""

    @abstractmethod
    def get_main_menu_current_selection(self):
        """Return the currently selected option in the main menu as a string.

        Returns
        -------
        str
            The text of the currently selected option in the main menu.
        """

    @abstractmethod
    def show_main_help_menu(self):
        """Display the help menu accessible from the main menu. Explains rules
        of the game."""

    @abstractmethod
    def hide_main_help_menu(self):
        """hide the help menu accessible from the main menu."""

    @abstractmethod
    def show_in_game_menu(self):
        """Show the in-game menu pop-up"""

    @abstractmethod
    def hide_in_game_menu(self):
        """Hide the in-game menu pop-up"""

    @abstractmethod
    def clear_short_QA_user_answer(self):
        """Clear the contents of the text entry box in the short answer Q&A
        widget."""

    @abstractmethod
    def set_true_or_false_QA_question(self, question_text):
        """Populate the true or false question and answer widget with the
        question contents.

        Parameters
        ----------
        question_text : str
            Question contents.
        """

    @abstractmethod
    def set_true_or_false_QA_options(self, options):
        """Populate the true or false question and answer widget with the
        specified options.

        Parameters
        ----------
        options : List
            List of strings to fill in as options.
        """

    @abstractmethod
    def show_short_QA_menu(self):
        """Show the short answer Q&A widget."""

    @abstractmethod
    def hide_short_QA_menu(self):
        """Hide the short answer Q&A widget."""

    @abstractmethod
    def show_true_or_false_QA_menu(self):
        """Show the true or false answer Q&A widget."""

    @abstractmethod
    def hide_true_or_false_QA_menu(self):
        """Hide the true or false answer Q&A widget."""

    @abstractmethod
    def select_true_or_false_QA_user_answer(self, option_index):
        """Select the option in the true of false QA widget with the text value
        given by `option` (should be "True" or "False").

        Parameters
        ----------
        option_index : int
            Index associated with desired option. Indices are zero-based and go
            left-to-right, top-to-bottom.
        """

    @abstractmethod
    def show_multiple_choice_QA_menu(self):
        """Show the multiple choice answer Q&A widget."""

    @abstractmethod
    def hide_multiple_choice_QA_menu(self):
        """Hide the multiple choice answer Q&A widget."""

    @abstractmethod
    def set_multiple_choice_QA_question(self, question_text):
        """Populate the multiple_choice answer question and answer widget with the
        question contents.

        Parameters
        ----------
        question_text : str
            Question contents.
        """

    @abstractmethod
    def set_multiple_choice_QA_hint(self, hint_text):
        """Fill in the hint portion of the multiple_choice question and answer widget
        with the hint contents.

        Parameters
        ----------
        hint_text : str
            Hint contents.
        """

    @abstractmethod
    def set_multiple_choice_QA_options(self, options):
        """Sets the options for selection to those in ``options``.

        Parameters
        ----------
        options : List
            List of strings comprising selection options.
        """

    @abstractmethod
    def select_multiple_choice_QA_user_answer(self, option_index):
        """Select the option in the multiple choice QA widget with the text
        value given by `option`.

        Parameters
        ----------
        option_index : int
            Index associated with desired option. Indices are zero-based and go
            left-to-right, top-to-bottom.
        """

    @abstractmethod
    def write_to_event_log(self, message):
        """Write a message on a new line in the event log widget.

        Parameters
        ----------
        message : str
            Text to write into the chat log.
        """

    @abstractmethod
    def clear_event_log(self):
        """Clear the contents of the event log."""

    @abstractmethod
    def reset_inventories(self):
        """Zero out and uncheck all adventurer inventory items in the
        display."""

    @abstractmethod
    def show_game_won_menu(self):
        """Display a pop-up to the user telling them they won the game."""

    @abstractmethod
    def hide_game_won_menu(self):
        """Hide the pop-up to the user telling them they won the game."""

    @abstractmethod
    def show_game_lost_died_menu(self):
        """
        Display a pop-up to the user telling them they lost the game from
        reaching 0 hitpoints.
        """

    @abstractmethod
    def hide_game_lost_died_menu(self):
        """
        Hide the pop-up to the user telling them they lost the game from
        reaching 0 hitpoints.
        """

    @abstractmethod
    def show_game_lost_trapped_menu(self):
        """
        Display a pop-up to the user telling them they lost the game from
        getting trapped in the maze.
        """

    @abstractmethod
    def hide_game_lost_trapped_menu(self):
        """
        Hide the pop-up to the user telling them they lost the game from
        getting trapped in the maze.
        """

    @abstractmethod
    def show_no_save_file_found_menu(self):
        """Show the pop-up telling the user that they can't load a game because
        no save file was found."""

    @abstractmethod
    def hide_no_save_file_found_menu(self):
        """Hide the pop-up telling the user that they can't load a game because
        no save file was found."""

    @abstractmethod
    def quit_entire_game(self):
        """Destroy the entire game and close the window"""
