import re
from .six import u


class DotfileModule(object):

    def __init__(self,  dirpath, contents):
        self.dirpath = dirpath
        self.contents = contents


class Dotdir(object):
    """Right now, this is pretty dumb, in that there can be only one dotfile
    directory, and no complicated merging happens.

    For example, suppose you have:

    dotfiles-a vim bundle A dotfiles-b vim bundle B

    The build directory will contain the last dotfile dir scanned, build vim
    bundle B

    And ~/.vim will symlink to build/dotfiles-b.

    As with dotfiles, dirs found in the dotfiles-user dir take precedence.

    So a scan of dotfiles-user vim bundle A dotfiles-z vim bundle B

    Will result in a symlink to the build dir containing `vim/bundle/A` from
    the dotfiles-user dir
    """

    def __init__(self,  dirname, dirpath):
        self.dirname = dirname
        self.dirpath = dirpath

    def update_dirpath(self, new_dirpath):
        if self.dirpath and re.match(r"\/dotfiles-user\/", self.dirpath):
            return
        self.dirpath = new_dirpath


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

    def add_file_at_path(self, dirpath, contents):
        dotfile = DotfileModule(dirpath, contents)
        if self.is_user_dotfile(dirpath):
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
