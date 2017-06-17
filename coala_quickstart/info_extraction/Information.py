from coala_quickstart.info_extraction.Info import Info


class LicenseUsedInfo(Info):
    description = "License of the project."
    value_type = (str,)
    example_values = ["MIT", "GPL-3", "Apache-2.0"]


class VersionInfo(Info):
    description = "Version information, see http://semver.org/"
    value_type = (str,)
    example_values = [">=1.2.7", "~1.2.3", "^0.2"]


class ProjectDependencyInfo(Info):
    description = "Dependency of the project."
    value_type = (str,)
    example_values = ['some_npm_package_name', 'some_gem_name', 'other_dep']

    def __init__(self,
                 source,
                 value,
                 extractor=None,
                 version=None,
                 url=''):
        super().__init__(source, value, extractor, version=version, url=url)


class PathsInfo(Info):
    description = "File path globs mentioned in the file."
    value_type = ([str],)
    example_values = ["**.py", "dev/tests/**"]


class IncludePathsInfo(PathsInfo):
    description = "Target files to perform analysis."


class IgnorePathsInfo(PathsInfo):
    description = "Files to ignore during analysis."


class ManFilesInfo(Info):
    description = "Filenames to put in place for the man program to find."
    value_type = (str, [str])
    example_values = ["./man/doc.1", ["./man/foo.1", "./man/bar.1"]]

    def __init__(self,
                 source,
                 value,
                 extractor=None,
                 keyword=""):
        """
        :param keyword: Primary keyword for ``man`` command that would display
                        the man pages provided in value argument.
        """
        super().__init__(source, value, extractor, keyword=keyword)
