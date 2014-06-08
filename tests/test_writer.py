from dotbuild.writer import Writer
from mock import patch
import os
import shutil
from . import TestCase


class WriterTests(TestCase):
    build_dir = "./build"
    filename = "./build/.inputrc"
    link = "./.inputrc"
    subd_filename = "./build/.subd/README"
    subd_link = "./.subd"

    def setUp(self):
        self._destroyFiles()
        self.writer = Writer([], ".inputrc", "\n3", True)
        self.writer.home_dirpath = "./"
        self.subd_writer = Writer([".subd"], "README", "\n2", True)
        self.subd_writer.home_dirpath = "./"

    def tearDown(self):
        self._destroyFiles()

    def _destroyFiles(self):
        if Writer._path_exists(self.filename):
            os.remove(self.filename)
        if Writer._path_exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        if Writer._path_exists(self.link):
            os.unlink(self.link)
        if Writer._path_exists(self.subd_link):
            os.unlink(self.subd_link)

    def test_writepath(self):
        self.assertEqual(self.writer._writepath(),
                         os.path.abspath(self.filename))

    def test_symlinkpath(self):
        writer = Writer([], ".inputrc", "\n3", True)
        self.assertEqual(writer._symlink_link_path(),
                         os.path.join(os.environ.get('HOME'), ".inputrc"))

        expected_path = os.path.abspath(os.path.join(writer.build_dirpath,
                                                     ".inputrc"))
        self.assertEqual(writer._symlink_source_path(),
                         expected_path)
        writer = Writer([".subd"], ".inputrc", "\n3", True)
        self.assertEqual(writer._symlink_link_path(),
                         os.path.join(os.environ.get('HOME'), ".subd"))
        expected_path = os.path.abspath(os.path.join(writer.build_dirpath,
                                                     ".subd"))
        self.assertEqual(writer._symlink_source_path(),
                         expected_path)

    def test_write(self):
        self.writer.write()
        with open(self.filename) as f:
            self.assertEqual(f.read(), "\n3")

        self.assertTrue(os.path.islink(self.link))

    def test_write_subd(self):
        self.subd_writer.write()

        with open(self.subd_filename) as f:
            self.assertEqual(f.read(), "\n2")

        self.assertTrue(os.path.islink(self.subd_link))

    def test_no_overwrite(self):
        with open(self.link, 'w+') as f:
            f.write('hi')

        with patch('dotbuild.writer.get_input', get_no_input):
            self.writer.write()
        with open(self.link) as f:
            self.assertEqual(f.read(), "hi")

        self.assertFalse(os.path.islink(self.link))

    def test_overwrite(self):
        with open(self.link, 'w+') as f:
            f.write('hi')

        with patch('dotbuild.writer.get_input', get_yes_input):
            self.writer.write()
        with open(self.link) as f:
            self.assertEqual(f.read(), "\n3")

        self.assertTrue(os.path.islink(self.link))


def get_yes_input(*args, **kwargs):
    return "y"


def get_no_input(*args, **kwargs):
    return "n"
