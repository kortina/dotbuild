# from mock import patch
from dotbuild.reader import Reader
from . import TestCase


class ReaderTests(TestCase):
    def test_recognize_prefix(self):
        reader = Reader(".")
        self.assertTrue(reader._dir_has_dotfiles_prefix("./dotfiles-user"))
        self.assertFalse(reader._dir_has_dotfiles_prefix("ndotfiles-user"))
