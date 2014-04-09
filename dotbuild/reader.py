from collections import defaultdict
import os
import re


class Reader(object):
    # filemap keys
    MODULES = 'modules'
    USER = 'user'
    NAME = 'name'
    CONTENTS = 'contents'

    def __init__(self,  dotfiles_dir):
        self.dotfiles_dir = dotfiles_dir
        self.file_map = defaultdict(lambda: {self.MODULES: []})

    def _dir_has_dotfiles_prefix(self, name):
        return re.match(r"^\.\/dotfiles-", name) is not None

    def _dir_is_user_dotfiles(self, name):
        return name == "./dotfiles-user"

    def _contents(self, dirname, filename):
        filepath = os.path.join(dirname, filename)
        with open(filepath, 'r') as f:
            contents = f.read()
        return contents

    def _file_map(self):
        for item in os.walk(self.dotfiles_dir):
            dirname = item[0]
            if not self._dir_has_dotfiles_prefix(dirname):
                continue
            for filename in item[2]:
                new = {self.NAME: dirname,
                       self.CONTENTS: self._contents(dirname, filename)}
                if self._dir_is_user_dotfiles(dirname):
                    self.file_map[filename][self.USER] = new
                else:
                    self.file_map[filename][self.MODULES].append(new)
