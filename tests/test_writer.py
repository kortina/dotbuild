from dotbuild.writer import Writer
from mock import patch
from mocks import get_no_input, get_yes_input
import os
import shutil
from . import TestCase


class WriterTests(TestCase):
    build_dir = "./build"
    filename = "./build/inputrc"
    link = "./.inputrc"

    def setUp(self):
        self._destroyFiles()
        self.writer = Writer("inputrc", "\n3", ".inputrc", True)
        self.writer.home_dirpath = "./"

    def tearDown(self):
        self._destroyFiles()

    def _destroyFiles(self):
        if Writer._path_exists(self.filename):
            os.remove(self.filename)
        if Writer._path_exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        if Writer._path_exists(self.link):
            os.unlink(self.link)

    def test_filepath(self):
        self.assertEqual(self.writer._filepath(),
                         os.path.abspath(self.filename))

    def test_symlinkpath(self):
        writer = Writer("inputrc", "\n3", ".inputrc", True)
        self.assertEqual(writer._symlinkpath(),
                         os.path.join(os.environ.get('HOME'), ".inputrc"))

    def test_write(self):
        self.writer.write()
        with open(self.filename) as f:
            self.assertEqual(f.read(), "\n3")

        self.assertTrue(os.path.islink(self.link))

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
