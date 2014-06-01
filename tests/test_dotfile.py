from dotbuild.dotfile import Dotfile
from . import TestCase


class DotfileTests(TestCase):
    def test_recognize_prefix(self):
        self.assertTrue(Dotfile.has_dotfiles_prefix("./dotfiles-user"))
        self.assertTrue(Dotfile.has_dotfiles_prefix("./dotfiles-team"))
        self.assertFalse(Dotfile.has_dotfiles_prefix("ndotfiles-user"))
        self.assertTrue(Dotfile.is_user_dotfile("./dotfiles-user"))
        self.assertFalse(Dotfile.is_user_dotfile("./dotfiles-team"))

    def test_aggregate(self):
        d = Dotfile("inputrc")
        d.add_file_from_source("./dotfiles-a", "1")
        d.add_file_from_source("./dotfiles-user", "3")
        d.add_file_from_source("./dotfiles-z", "2")
        self.assertEqual(d.aggregated_contents(), "\n1\n2\n3")
