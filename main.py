from mock import TextTriviaMazeModel  # FIXME: Set to real model module
from text_trivia_maze_controller import TextTriviaMazeController

if __name__ == "__main__":
    maze_model = TextTriviaMazeModel()

    # NOTE: The controller will create a view object internally
    maze_controller = TextTriviaMazeController(maze_model)

    # Register observers to model
    maze_model.register_observer(maze_controller)

    # Start the main event loop
    maze_controller.start_main_event_loop()
