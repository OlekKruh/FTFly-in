import sys
from typing import NoReturn


def error_exit(message: str) -> NoReturn:
    """
    Terminates the program execution with an error code (1).

    Prints a custom error message to the console before exiting.
    Used to handle critical failures, such as invalid command-line
    arguments or file reading errors.

    Args:
        message (str): The text describing the cause of the error.
    """
    print(f"Error Exit >>> {message}")
    sys.exit(1)


def end_exit() -> NoReturn:
    """
    Gracefully terminates the program execution with a success code (0).

    Prints a farewell message to the console before exiting. Used for a normal,
    scheduled shutdown of the application.
    """
    print("Program closed. Have a nice day.")
    sys.exit(0)
