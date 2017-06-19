import re

from coala_quickstart.info_extraction.InfoExtractor import InfoExtractor
from coala_quickstart.info_extraction.Information import (
    IndentStyleInfo, IndentSizeInfo, TrailingWhitespaceInfo, FinalNewlineInfo,
    CharsetInfo, LineBreaksInfo)


class EditorconfigInfoExtractor(InfoExtractor):
    supported_file_globs = (".editorconfig",)

    spec_references = [
        "http://editorconfig.org/#file-format-details",
        "https://gitlab.com/coala/GSoC-2017/issues/172"]

    supported_info_kinds = (
        IndentStyleInfo, IndentSizeInfo, TrailingWhitespaceInfo,
        FinalNewlineInfo, CharsetInfo, LineBreaksInfo)

    def parse_file(self, fname, file_content):

        # Regular expressions for parsing section header.
        SECTRE = re.compile(
            r"""

            \s *                                # Optional whitespace
            \[                                  # Opening square brace

            (?P<header>                         # One or more chars excluding
                ( [^\#;] | \\\# | \\; ) +       # unescaped # and ; characters
            )

            \]                                  # Closing square brace

            """, re.VERBOSE
        )
        # Regular expression for parsing option name/values.
        OPTRE = re.compile(
            r"""

            \s *                                # Optional whitespace
            (?P<option>                         # One or more chars excluding
                [^:=\s]                         # : a = characters (and first
                [^:=] *                         # must not be whitespace)
            )
            \s *                                # Optional whitespace
            (?P<vi>
                [:=]                            # Single = or : character
            )
            \s *                                # Optional whitespace
            (?P<value>
                . *                             # One or more characters
            )
            $

            """, re.VERBOSE
        )

        in_section = False
        current_section = None
        config = {}
        with open(fname, encoding='utf-8') as fp:
            line = fp.readline()
            if line.startswith(str('\ufeff')):
                line = line[1:]  # Strip UTF-8 BOM

            while True:
                # a section header or option header?
                match_object = SECTRE.match(line)
                if match_object:
                    section_name = match_object.group('header')
                    config[section_name] = {}
                    current_section = section_name
                    in_section = True
                    optname = None
                else:
                    match_object = OPTRE.match(line)
                    if match_object:
                        optname, vi, optval = match_object.group(
                            'option', 'vi', 'value')
                        if ';' in optval or '#' in optval:
                            # ';' and '#' are comment delimiters only if
                            # preceeded by a spacing character
                            mo = re.search('(.*?) [;#]', optval)
                            if mo:
                                optval = mo.group(1)
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''
                        optname = optname.rstrip().lower()
                        if in_section:
                            config[current_section][optname] = optval
                    else:
                        # unrecognized line type.
                        pass
                line = fp.readline()
                if not line:
                    break
                # comment or blank line?
                while line.strip() == '' or line[0] in '#;':
                    line = fp.readline()

        return config

    def find_information(self, fname, parsed_file):
        results = []

        for target_pattern, config in parsed_file.items():
            for key, value in config.items():
                if key == "indent_size":
                    if value == "tab":
                        #  When set to "tab", the value of tab_width
                        # (if specified) will be used
                        if config.get("tab_width"):
                            results.append(
                                IndentSizeInfo(
                                    fname,
                                    int(config["tab_width"]),
                                    scope=target_pattern))
                    else:
                        results.append(
                            IndentSizeInfo(
                                fname, int(value), scope=target_pattern))
                if key == "indent_style":
                    results.append(
                        IndentStyleInfo(fname, value, scope=target_pattern))
                if key == "trim_trailing_whitespace":
                    if value == "true":
                        results.append(
                            TrailingWhitespaceInfo(
                                fname, True, scope=target_pattern))
                    if value == "false":
                        results.append(
                            TrailingWhitespaceInfo(
                                fname, False, scope=target_pattern))
                if key == "insert_final_newline":
                    if value == "true":
                        results.append(
                            FinalNewlineInfo(
                                fname, True, scope=target_pattern))
                    if value == "false":
                        results.append(
                            FinalNewlineInfo(
                                fname, False, scope=target_pattern))
                if key == "charset":
                    results.append(
                        CharsetInfo(fname, value, scope=target_pattern))
                if key == "end_of_line":
                    results.append(
                        LineBreaksInfo(fname, value, scope=target_pattern))

        return results
