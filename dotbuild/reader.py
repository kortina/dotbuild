import os
from .dotfile import Dotfile, DotfileMap


class Reader(object):

    def __init__(self,  dotfiles_dir):
        self.dotfiles_dir = dotfiles_dir
        self.dotfiles = DotfileMap()

    def _contents(self, source_dirpath, filename):
        filepath = os.path.join(source_dirpath, filename)
        with open(filepath, 'r') as f:
            contents = f.read()
        return contents

    def read(self):
        """
        scan for dotfiles in current working directory and generate dictionary
        to store all of the filenames and content

        """
        for item in os.walk(self.dotfiles_dir):
            source_dirpath = item[0]
            if not Dotfile.has_dotfiles_prefix(source_dirpath):
                continue
            for filename in item[2]:
                contents = self._contents(source_dirpath, filename)
                self.dotfiles.add(source_dirpath, filename, contents)
