import sys


def error_exit(message: str) -> None:
    print(f"Error Exit >>> {message}")
    sys.exit(1)


def end_exit() -> None:
    print("Program closet. Have a nice day.")
    sys.exit(0)
