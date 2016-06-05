import os
from collections import defaultdict

from coala_utils.Extensions import exts


def split_by_language(project_files):
    """
    Splits the given files based on language. This ignores unknown extensions.

    :param project_files: A list of file paths.
    :return:              A dict with language name as keys and a list of
                          files coming under that language as values.
    """
    lang_files = defaultdict(lambda: set())
    for file in project_files:
        name, ext = os.path.splitext(file)
        if ext in exts:
            for lang in exts[ext]:
                lang_files[lang.lower()].add(file)
                lang_files["all"].add(file)

    return lang_files


def get_extensions(project_files):
    """
    Generates the extensions available in the given project files.

    :param project_files: A list of file paths.
    :return:              The set of extensions used in the project_files
                          for which bears exist.
    """
    extset = defaultdict(lambda: set())
    for file in project_files:
        ext = os.path.splitext(file)[1]
        if ext in exts:
            for lang in exts[ext]:
                extset[lang.lower()].add(ext)

    return extset
