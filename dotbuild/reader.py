import os
from .dotfile import Dotfile


class Reader(object):

    def __init__(self,  dotfiles_dir):
        self.dotfiles_dir = dotfiles_dir
        self.dotfiles = {}

    def _contents(self, dirpath, filename):
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'r') as f:
            contents = f.read()
        return contents

    def read(self):
        """
        scan for dotfiles in current working directory and generate dictionary
        to store all of the filenames and content

        """
        for item in os.walk(self.dotfiles_dir):
            dirpath = item[0]
            if not Dotfile.has_dotfiles_prefix(dirpath):
                continue
            for filename in item[2]:
                contents = self._contents(dirpath, filename)
                if not filename in self.dotfiles.keys():
                    self.dotfiles[filename] = Dotfile(filename)
                self.dotfiles[filename].add_file_at_path(dirpath, contents)
