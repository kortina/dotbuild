import os


class Writer(object):

    def __init__(self, filename, contents, symlink):
        self.filename = filename
        self.contents = contents
        self.build_dirpath = "./build"
        self.symlink = symlink
        self.home_dirpath = os.environ.get('HOME')

    def _create_build_dir(self):
        if not os.path.exists(self.build_dirpath):
            os.makedirs(self.build_dirpath)

    def _filepath(self):
        return os.path.join(self.build_dirpath, self.filename)

    def _symlinkpath(self):
        return os.path.join(self.home_dirpath, self.symlink)

    def _remove_symlink(self):
        if os.path.exists(self._symlinkpath()):
            os.unlink(self._symlinkpath())

    def _create_symlink(self):
        self._remove_symlink()
        os.symlink(self._filepath(), self._symlinkpath())

    def write(self):
        self._create_build_dir()
        f = open(self._filepath(), 'w+')
        f.write(self.contents)
        f.close()
        self._create_symlink()
