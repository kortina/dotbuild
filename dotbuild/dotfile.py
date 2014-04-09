import re


class DotfileModule(object):

    def __init__(self,  dirpath, contents):
        self.dirpath = dirpath
        self.contents = contents


class Dotfile(object):

    def __init__(self,  filename):
        self.name = filename
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
