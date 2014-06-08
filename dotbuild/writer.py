import logging
import os
import sys


def get_input(*args, **kwargs):
    if sys.version_info[0] >= 3:
        return input(*args, **kwargs)
    else:
        return raw_input(*args, **kwargs)


class Writer(object):

    def __init__(self, dirpath, filename, contents, confirm_overwrite):
        self.dirpath = dirpath
        self.filename = filename
        self.contents = contents
        self.build_dirpath = "./build"
        self.home_dirpath = os.environ.get('HOME')
        self.confirm_overwrite = confirm_overwrite

    def _create_build_dir(self):
        if not os.path.exists(self.build_dirpath):
            os.makedirs(self.build_dirpath)

    def _writepath(self):
        path = [self.build_dirpath]
        if self.dirpath:
            path += self.dirpath
        path += [self.filename]
        return os.path.abspath(os.path.join(*path))

    def _create_containing_dirs(self):
        if not self.dirpath:
            return
        path = os.path.join(*self.dirpath)
        path = os.path.join(self.build_dirpath, path)
        if not os.path.exists(path):
            os.makedirs(path)

    def _is_in_subd(self):
        return len(self.dirpath) > 0

    def _symlink_source_path(self):
        # built file or top subdirectoy in the build directory containing the
        # path to the built file
        if not self._is_in_subd():
            # symlink directly to built file
            path = os.path.join(self.build_dirpath, self.filename)
        else:
            # symlink to a folder contianing the built file
            path = os.path.join(self.build_dirpath, self.dirpath[0])
        return os.path.abspath(path)

    def _symlink_link_path(self):
        # file of link in user home directory pointing to built file or
        # directory containing the built file
        if not self._is_in_subd():
            # symlink directly to built file
            return os.path.join(self.home_dirpath, self.filename)
        else:
            # symlink to a folder contianing the built file
            return os.path.join(self.home_dirpath, self.dirpath[0])

    @staticmethod
    def _path_exists(path):
        """Checks for a file, live symlink, or dead symlink at given path."""
        return os.path.exists(path) or os.path.islink(path)

    def _symlink_link_exists(self):
        return self._path_exists(self._symlink_link_path())

    def _remove_symlink(self):
        if self._symlink_link_exists():
            os.unlink(self._symlink_link_path())

    def _create_symlink(self):
        # symlink from homedir to built file or directory containing built file
        if self._symlink_link_exists():
            if self.confirm_overwrite:
                msg = "{0} exists. OK to overwrite?"
                msg = msg.format(self._symlink_link_path())
                if not self._confirm(msg):
                    msg = "Skipping overwrite of {0}"
                    msg = msg.format(self._symlink_link_path())
                    logging.info(msg)
                    return
            self._remove_symlink()
        os.symlink(self._symlink_source_path(), self._symlink_link_path())
        msg = "Symlinked {0} to {1}"
        logging.info(msg.format(self._symlink_link_path(),
                                self._symlink_source_path()))

    def write(self):
        self._create_build_dir()
        self._create_containing_dirs()
        f = open(self._writepath(), 'w+')
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
