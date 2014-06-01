import re
from .six import u


class DotfileModule(object):

    def __init__(self,  dotfile_source, contents):
        self.dotfile_source = dotfile_source
        self.contents = contents


class Dotfile(object):

    def __init__(self,  filename):
        self.filename = filename
        self.linkname = u(".") + u(filename)
        self.dotfiles = []
        self.user_dotfile = None

    @staticmethod
    def has_dotfiles_prefix(name):
        return re.match(r"^\.\/dotfiles-", name) is not None

    @staticmethod
    def is_user_dotfile(name):
        return name == "./dotfiles-user"

    def add_file_from_source(self, dotfile_source, contents):
        dotfile = DotfileModule(dotfile_source, contents)
        if self.is_user_dotfile(dotfile_source):
            self.user_dotfile = dotfile
        else:
            self.dotfiles.append(dotfile)

    def _append_contents(self, contents, dotfile):
        if dotfile.contents:
            contents += u("\n")
            # need to string-escape so unicode doesn't break when it encounters
            # escaped chars like \] in a file
            contents += u(dotfile.contents.encode('string-escape'))
        return contents

    def aggregated_contents(self):
        contents = u("")
        for dotfile in self.dotfiles:
            contents = self._append_contents(contents, dotfile)

        # append the special user_dotfile last so it takes precedence
        if self.user_dotfile:
            contents = self._append_contents(contents, self.user_dotfile)

        return contents
