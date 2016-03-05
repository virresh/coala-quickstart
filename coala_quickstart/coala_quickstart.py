#!/usr/bin/env python3

from os.path import abspath, join


def get_project_dir():
    """
    Retrieves the project directory from the user:

    >>> from coalib.misc.ContextManagers import simulate_console_inputs
    >>> from coalib.misc.ContextManagers import suppress_stdout
    >>> with simulate_console_inputs("/abs/path"), suppress_stdout():
    ...     dir = get_project_dir()
    >>> assert dir == "/abs/path"

    If he doesn't feel like giving a directory, we'll assume the current
    directory:

    >>> with simulate_console_inputs(""), suppress_stdout():
    ...     dir = get_project_dir()
    >>> assert dir == abspath(".")
    """
    dir = input(
        "Hey fellow! Awesome you decided to do high quality coding. "
        "We hope we can help you with that. Let's get started, what is your "
        "project directory? We'll create a `.coafile` in there with some "
        "settings. Is the current directory fine? (press enter to confirm or "
        "enter the project directory) ")
    return abspath(dir)


def main():
    dir = get_project_dir()
    files_glob = input("Please enter the files glob: ")
    coafile = open(join(dir, ".coafile"), "a+")
