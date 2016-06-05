import os

from coala_utils.string_processing.StringConverter import StringConverter
from coala_utils.Question import ask_question
from coala_utils.Extensions import exts


def valid_path(path: StringConverter):
    """
    Raises an exception if the given ``StringConverter`` object is
    not a valid directory. Example:

    >>> from coala_utils.string_processing.StringConverter import (
    ...     StringConverter)
    >>> import os
    >>> valid_path(StringConverter("/tmp"))
    '/tmp'
    >>> os.getcwd() == valid_path(StringConverter(""))
    True
    >>> valid_path(StringConverter("invalid_dir"))
    Traceback (most recent call last):
      ...
    ValueError: The given path doesn't exist.

    :param path: A ``StringConverter`` object.
    :return:     The full expanded path if the path has relative elements.
    """
    path = os.path.abspath(os.path.expanduser(str(path)))
    if not os.path.isdir(path):
        raise ValueError("The given path doesn't exist.")
    return path
