from tkinter import *
from tkinter import messagebox
from question_and_answer import *
from qa_gui_widget_controller import QAGUIWidgetController


class QAGUIWidgetView:
    """
    This class represents the view for the Trivia Maze game.

    Attributes:
        controller (QAGUIWidgetController): The controller that the view interacts with.
        window (Tk): The Tkinter window object.
        question_label (Label): The label for displaying the question.
        options_frame (Frame): The frame for displaying answer options.
        option_buttons (list): A list of buttons for each answer option.
        input_frame (Frame): The frame for displaying the input field.
        input_field (Entry): The input field for player to enter answer.
        feedback_label (Label): The label for displaying feedback.

    Methods:
        set_controller(controller: QAGUIWidgetController): Sets the controller that the view interacts with.
        show_question(question: str, options: list): Shows the question and answer options.
        get_answer_input() -> str: Gets the player's answer input.
        show_feedback(feedback: str): Shows feedback to the player.
    """

    def __init__(self, window_title: str = "Trivia Maze"):
        """
        Initializes a QAGUIWidgetView object.

        Args:
            window_title (str): The title of the Tkinter window. Default is "Trivia Maze".
        """
        self.controller = None
        self.window = Tk()
        self.window.title(window_title)

        self.question_label = Label(self.window, text="", font=("Helvetica", 20), pady=10)
        self.question_label.pack()

        self.options_frame = Frame(self.window)
        self.options_frame.pack(pady=10)

        self.option_buttons = []

        self.input_frame = Frame(self.window)
        self.input_frame.pack(pady=10)

        self.input_field = Entry(self.input_frame, width=40, font=("Helvetica", 16))
        self.input_field.pack(side=LEFT)

        self.feedback_label = Label(self.window, text="", font=("Helvetica", 16), pady=10)
        self.feedback_label.pack()

    def set_controller(self, controller: QAGUIWidgetController):
        """
        Sets the controller that the view interacts with.

        Args:
            controller (QAGUIWidgetController): The controller that the view interacts with.
        """
        self.controller = controller

    def show_question(self, question: str, options: list):
        """
        Shows the question and answer options.

        Args:
            question (str): The question to be displayed.
            options (list): A list of answer options to be displayed.
        """
        self.question_label.config(text=question)
        self.options_frame.pack_forget()

        self.option_buttons = []
        for option in options:
            button = Button(self.options_frame, text=option, font=("Helvetica", 16), command=lambda option=option: self.controller.handle_option(option))
            button.pack(side=LEFT, padx=5)
            self.option_buttons.append(button)

        self.input_frame.pack_forget()
        self.input_field.delete(0, END)

    def show_options(self, options):
        """
        Shows the answer option labels based on the type of question.

        Args:
            options (List[str]): The list of options for the question.
        """
        if len(options) == 2:
            self.option_labels[0].config(text="True")
            self.option_labels[1].config(text="False")
        else:
            for i in range(len(options)):
                self.option_labels[i].config(text=options[i])

    def show_feedback(self, correct: bool):
        """
        Shows feedback to the player indicating whether their answer is correct or incorrect.

        Args:
            correct (bool): True if the player's answer is correct, False otherwise.
        """
        if correct:
            self.feedback_label.config(text="Correct!")
        else:
            self.feedback_label.config(text="Incorrect")

    def clear_widget(self):
        """
        Clears the widget.
        """
        self.question_label.destroy()
        for choice in self.answer_options:
            choice.destroy()
        self.answer_options = []
        if self.answer_entry:
            self.answer_entry.destroy()
        self.answer_entry = None
        self.submit_button.destroy()

    def show_message(self, message: str):
        """
        Shows a message in the widget.

        Args:
            message (str): The message to be shown.
        """
        messagebox.showinfo("Feedback", message)

    def start(self):
        """
        Starts the widget.
        """
        self.root.mainloop()

