import re


class Reader(object):

    def __init__(self,  dotfiles_dir):
        self.dotfiles_dir = dotfiles_dir

    def _dir_has_dotfiles_prefix(self, name):
        return re.match(r"^\.\/dotfiles-", name) is not None
