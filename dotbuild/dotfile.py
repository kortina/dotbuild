import os
import re
from .six import u


class DotfileMap(object):
    """Map of source dirpaths + filenames to aggregated file contents.

    eg,
    {".vim/bundle/pep8/README": "hello world"}
    """

    def __init__(self):
        self.files = {}

    @staticmethod
    def _parse_dirpath(source_dirpath):
        """
        Extract the source source_module name and dirpath from the
        source_dirpath.

        eg, given:
            ./dotfiles-user/vim/bundle/pep8
        return the tuple (source_module, dirpath)
            "dotfiles-user", ["vim", "bundle", pep8"]

        `source_module` is the name of the dotfile source_module, and `dirpath`
        is the directory path within that module that will written to the user
        home direcotry.
        """
        parts = source_dirpath.split(os.sep)
        # [0] is always "."
        return parts[1], parts[2:]

    @staticmethod
    def keyname(dirpath, filename):
        return os.sep.join(dirpath + [filename])

    def __getitem__(self, keyname):
        """convenience accessor for items in self.files"""
        return self.files[keyname]

    def add(self, source_dirpath, source_filename, contents):
        source_module, dirpath = self._parse_dirpath(source_dirpath)
        keyname = self.keyname(dirpath, source_filename)
        if not keyname in self.files:
            self.files[keyname] = Dotfile(dirpath, source_filename)
        self.files[keyname].add_contents_from_source(source_module, contents)

    def next_dotfile(self):
        """iterate through filemap, yield next pair,
        filename, dotfile
        """
        for dotfile in self.files.values():
            yield dotfile


class Dotfile(object):

    def __init__(self,  dirpath, filename):
        self.filename = filename
        self.dirpath = dirpath
        self.contents = []
        self.user_contents = u("")

    @staticmethod
    def has_dotfiles_prefix(name):
        return re.match(r"^\.\/dotfiles-", name) is not None

    @staticmethod
    def is_user_source(name):
        return name == "dotfiles-user"

    def add_contents_from_source(self, source_module,
                                 contents):
        # need to string-escape so unicode doesn't break when it encounters
        # escaped chars like \] in a file
        contents = u(contents.encode('string-escape'))
        if self.is_user_source(source_module):
            self.user_contents = contents
        else:
            self.contents.append(contents)

    def aggregated_contents(self):
        # combine contents from all sources.
        # ensure user_contents takes precedence by adding to bottom
        return u("\n").join(self.contents + [self.user_contents])
