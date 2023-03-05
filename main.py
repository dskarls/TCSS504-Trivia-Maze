"""
Entry point (driver) for game. Run this module directly from the command line
to play the game.
"""
import pathlib

from trivia_maze import TriviaMaze
from text_trivia_maze_controller import TextTriviaMazeController

if __name__ == "__main__":
    # Dimensions of maze
    NUM_ROWS = 5
    NUM_COLS = 7

    # The file containing the raw data used to initialize the database
    DB_FILE_PATH = pathlib.Path("db") / "Lone_Rangers_QA_DB.csv"

    maze_model = TriviaMaze(NUM_ROWS, NUM_COLS, DB_FILE_PATH)

    # NOTE: The controller will create a view object internally
    maze_controller = TextTriviaMazeController(maze_model)

    # Start the main event loop
    maze_controller.start_main_event_loop()
