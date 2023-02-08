"""
Classes for a console-based GUI
"""
import curses
import math


class TerminalTooSmall(RuntimeError):
    """If the user's terminal window is too small to display the game"""


class ConsoleWindow:
    def __init__(self, x0, y0, width, height, color):
        """Note that no refresh of the subwindow display is performed upon
        initialization, so it won't show up unless you manually refresh it."""
        # Create curses window obj
        self.__window = curses.newwin(height, width, y0, x0)
        self.__window.bkgd(" ", color)
        self.__window.keypad(True)
        self.color = color

        # Calculate approximate center
        self.center = [
            math.floor(width / 2.0),
            math.floor(height / 2.0),
        ]

    def add_text_at_pos(self, x, y, text, text_and_bg_color, bold=True):
        # Add the string to the center, with BOLD flavoring.
        text_flags = (
            text_and_bg_color | curses.A_BOLD if bold else text_and_bg_color
        )

        self.__window.addstr(y, x, text, text_flags)
        self.refresh()

    def clear(self):
        self.__window.clear()

    def refresh(self):
        self.__window.refresh()

    def get_player_input(self):
        return self.__window.getch()


class ConsoleTriviaMazeView:
    __MIN_WIDTH = 60
    __MIN_HEIGHT = 20

    def __init__(self):
        self.__colors = self.__initialize_graphics_backend()

        self.__windows = self.__initialize_windows()

    def __confirm_terminal_size_large_enough(self):
        if curses.COLS < self.__MIN_WIDTH:
            raise TerminalTooSmall("Please increase the size of your terminal")

        if curses.LINES < self.__MIN_HEIGHT:
            raise TerminalTooSmall("Please increase the size of your terminal")

    def __initialize_graphics_backend(self):
        # Initialize curses
        stdscr = curses.initscr()

        # Confirm that terminal is large enough
        self.__confirm_terminal_size_large_enough()

        stdscr.clear()
        stdscr.refresh()

        # Start color, too.  Harmless if the terminal doesn't have
        # color; user can test with has_color() later on.  The try/catch
        # works around a minor bit of over-conscientiousness in the curses
        # module -- the error return from C start_color() is ignorable.
        if curses.has_colors():
            curses.start_color()

        # Turn off blinking cursor
        curses.curs_set(False)

        # Create a list of all the colors except for black and white. These
        # will server as the background colors for the windows. Because these
        # constants are defined in ncurses, we can't create the list until
        # after the curses.initscr call:
        return self.__initialize_colors()

    def __initialize_colors(self):
        base_colors = [
            curses.COLOR_BLUE,
            curses.COLOR_CYAN,
            curses.COLOR_GREEN,
            curses.COLOR_MAGENTA,
            curses.COLOR_RED,
            curses.COLOR_YELLOW,
        ]

        curses_colors = []
        for ind, color in enumerate(base_colors):
            curses.init_pair(ind + 1, curses.COLOR_WHITE, color)
            curses_colors.append(curses.color_pair(ind + 1))

        return curses_colors

    def __initialize_windows(self):
        MAP_WIDTH = int(0.8 * curses.COLS)
        MAP_HEIGHT = int(0.8 * curses.LINES)
        HP_GAUGE_HEIGHT = 3

        # Map window
        map_window_args = {
            "x0": 0,
            "y0": 0,
            "width": MAP_WIDTH,
            "height": MAP_HEIGHT,
            "color": self.__colors[0],
        }
        map_window = ConsoleWindow(**map_window_args)
        map_window_text = "Map"
        map_window.add_text_at_pos(
            *map_window.center, map_window_text, map_window_args["color"]
        )

        # HP Gauge
        hp_gauge_window_args = {
            "x0": MAP_WIDTH,
            "y0": 0,
            "width": curses.COLS - MAP_WIDTH,
            "height": HP_GAUGE_HEIGHT,
            "color": self.__colors[1],
        }
        hp_gauge_window = ConsoleWindow(**hp_gauge_window_args)
        hp_gauge_window_text = "HP gauge"
        hp_gauge_window.add_text_at_pos(
            hp_gauge_window.center[0] - 3,
            hp_gauge_window.center[1],
            hp_gauge_window_text,
            hp_gauge_window_args["color"],
        )

        # Legend and/or inventory?
        inventory_window_args = {
            "x0": MAP_WIDTH,
            "y0": HP_GAUGE_HEIGHT,
            "width": curses.COLS - MAP_WIDTH,
            "height": MAP_HEIGHT - HP_GAUGE_HEIGHT,
            "color": self.__colors[2],
        }
        inventory_window_text = (
            "Inventory\n (pillars of OOP,\n      potions,\n       keys)"
        )
        inventory_window = ConsoleWindow(**inventory_window_args)
        inventory_window.add_text_at_pos(
            inventory_window.center[0] - 3,
            inventory_window.center[1],
            inventory_window_text,
            inventory_window_args["color"],
        )

        # Output log (probably make this a scrollable pad?)
        event_log_window_args = {
            "x0": 0,
            "y0": MAP_HEIGHT,
            "width": curses.COLS,
            "height": curses.LINES - MAP_HEIGHT,
            "color": self.__colors[3],
        }
        event_log_window_text = "Output log (notifies users of items picked up, damage taken, potions used, etc)"
        event_log_window = ConsoleWindow(
            **event_log_window_args,
        )
        event_log_window.add_text_at_pos(
            event_log_window.center[0] - len(event_log_window_text) // 2,
            event_log_window.center[1],
            event_log_window_text,
            event_log_window_args["color"],
        )

        # Trivia dialog pop-up
        #    trivia_dialog_width = int(0.7 * curses.COLS)
        #    trivia_dialog_height = int(0.4 * curses.LINES)
        #    trivia_dialog_x = (curses.COLS - trivia_dialog_width) // 2
        #    trivia_dialog_y = (curses.LINES - trivia_dialog_height) // 2
        #    trivia_dialog_colors = curses.color_pair(4)
        #    trivia_dialog_text = "Trivia dialog"
        #    trivia_dialog = SubWindow(
        #        trivia_dialog_x,
        #        trivia_dialog_y,
        #        trivia_dialog_width,
        #        window3_height,
        #        window3_colors,
        #    )
        #    trivia_dialog.add_text_at_pos(
        #        trivia_dialog.center[0] - len(window3_text) // 2,
        #        trivia_dialog.center[1],
        #        trivia_dialog_text,
        #        trivia_dialog_colors,
        #    )

        # Main menu pop-up
        # in_game_menu_window_width = int(0.5 * curses.COLS)
        # in_game_menu_window_height = int(0.75 * curses.LINES)
        # in_game_menu_window_x = (curses.COLS - in_game_menu_window_width) // 2
        # in_game_menu_window_y = (curses.LINES - in_game_menu_window_height) // 2
        # in_game_menu_window_colors = curses.color_pair(6)
        # in_game_menu_window_text = "In-game menu"
        # in_game_menu_window = ConsoleWindow(
        #    in_game_menu_window_x,
        #    in_game_menu_window_y,
        #    in_game_menu_window_width,
        #    in_game_menu_window_height,
        #    in_game_menu_window_colors,
        # )
        # in_game_menu_window.add_text_at_pos(
        #    in_game_menu_window.center[0] - len(in_game_menu_window_text) // 2,
        #    in_game_menu_window.center[1],
        #    in_game_menu_window_text,
        #    in_game_menu_window_colors,
        # )

        return [
            map_window,
            hp_gauge_window,
            inventory_window,
            event_log_window,
        ]

    @staticmethod
    def __main(_, window: ConsoleWindow):
        player_input = None
        while player_input != 27:  # FIXME: Using ESC to quit window for now
            # Retrieve keyboard input
            player_input = window.get_player_input()

            window.clear()
            window.add_text_at_pos(
                *window.center,
                f"You entered the following key: {player_input}",
                window.color,
            )

    def __enter__(self):
        # We can use any window to grab player input, so just pass the first
        # one created (which is assumed to exist)
        curses.wrapper(self.__main, self.__windows[0])

    def __exit__(self, type_, value, traceback):
        # curses.wrapper already handles cleanup, so we only need to define
        # this method to make Python happy
        pass


if __name__ == "__main__":
    with ConsoleTriviaMazeView():
        pass
