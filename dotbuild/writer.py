import logging
import os
import sys


def get_input(*args, **kwargs):
    if sys.version_info[0] >= 3:
        return input(*args, **kwargs)
    else:
        return raw_input(*args, **kwargs)


class Writer(object):

    def __init__(self, filename, contents, symlink, confirm_overwrite):
        self.filename = filename
        self.contents = contents
        self.build_dirpath = "./build"
        self.symlink = symlink
        self.home_dirpath = os.environ.get('HOME')
        self.confirm_overwrite = confirm_overwrite

    def _create_build_dir(self):
        if not os.path.exists(self.build_dirpath):
            os.makedirs(self.build_dirpath)

    def _filepath(self):
        return os.path.abspath(os.path.join(self.build_dirpath, self.filename))

    def _symlinkpath(self):
        return os.path.join(self.home_dirpath, self.symlink)

    @staticmethod
    def _path_exists(path):
        """Checks for a file, live symlink, or dead symlink at given path."""
        return os.path.exists(path) or os.path.islink(path)

    def _symlink_path_exists(self):
        return self._path_exists(self._symlinkpath())

    def _remove_symlink(self):
        if self._symlink_path_exists():
            os.unlink(self._symlinkpath())

    def _create_symlink(self):
        if self._symlink_path_exists():
            if self.confirm_overwrite:
                msg = "{0} exists. OK to overwrite?"
                msg = msg.format(self._symlinkpath())
                if not self._confirm(msg):
                    msg = "Skipping overwrite of {0}"
                    msg = msg.format(self._symlinkpath())
                    logging.info(msg)
                    return
            self._remove_symlink()
        os.symlink(self._filepath(), self._symlinkpath())
        logging.info("Symlinked {0} to {1}".format(self._symlinkpath(),
                                                   self._filepath()))

    def write(self):
        self._create_build_dir()
        f = open(self._filepath(), 'w+')
        # need to utf8 encode writing so we don't fail when writing unicode
        # chars
        f.write(self.contents.encode('utf8'))
        f.close()
        self._create_symlink()

    def _confirm(self, message):

        yes = set(['yes', 'y', 'ye', ''])
        choice = get_input("{0}\n[Y\\n]".format(message)).lower()
        if choice in yes:
            return True
        else:
            return False
