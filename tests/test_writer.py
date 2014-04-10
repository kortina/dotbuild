from dotbuild.writer import Writer
import os
from . import TestCase


class WriterTests(TestCase):
    build_dir = "./build"
    filename = "./build/inputrc"
    link = "./.inputrc"

    def tearDown(self):
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.build_dir):
            os.removedirs(self.build_dir)
        if os.path.exists(self.link):
            os.unlink(self.link)

    def test_filepath(self):
        w = Writer("inputrc", "\n3", ".inputrc")
        self.assertEqual(w._filepath(), self.filename)

    def test_symlinkpath(self):
        w = Writer("inputrc", "\n3", ".inputrc")
        self.assertEqual(w._symlinkpath(),
                         os.path.join(os.environ.get('HOME'), ".inputrc"))

    def test_write(self):
        w = Writer("inputrc", "\n3", ".inputrc")
        w.home_dirpath = "./"
        w.write()
        with open(self.filename) as f:
            self.assertEqual(f.read(), "\n3")

        self.assertTrue(os.path.islink(self.link))
