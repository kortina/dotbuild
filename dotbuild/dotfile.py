import re
from .six import u


class DotfileModule(object):

    def __init__(self,  dirpath, contents):
        self.dirpath = dirpath
        self.contents = contents


class Dotfile(object):

    def __init__(self,  filename):
        self.name = filename
        self.filename = u(".") + u(filename)
        self.dotfiles = []
        self.user_dotfile = None

    @staticmethod
    def has_dotfiles_prefix(name):
        return re.match(r"^\.\/dotfiles-", name) is not None

    @staticmethod
    def is_user_dotfile(name):
        return name == "./dotfiles-user"

    def add_file_at_path(self, dirpath, contents):
        dotfile = DotfileModule(dirpath, contents)
        if self.is_user_dotfile(dirpath):
            self.user_dotfile = dotfile
        else:
            self.dotfiles.append(dotfile)

    def _append_contents(self, contents, dotfile):
        if dotfile.contents:
            contents += u("\n")
            contents += u(dotfile.contents)
        return contents

    def aggregated_contents(self):
        contents = u("")
        for dotfile in self.dotfiles:
            contents = self._append_contents(contents, dotfile)

        # append the special user_dotfile last so it takes precedence
        if self.user_dotfile:
            contents = self._append_contents(contents, self.user_dotfile)

        return contents
