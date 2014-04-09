from dotbuild.dotfile import Dotfile
from . import TestCase


class DotfileTests(TestCase):
    def test_recognize_prefix(self):
        self.assertTrue(Dotfile.has_dotfiles_prefix("./dotfiles-user"))
        self.assertTrue(Dotfile.has_dotfiles_prefix("./dotfiles-team"))
        self.assertFalse(Dotfile.has_dotfiles_prefix("ndotfiles-user"))
        self.assertTrue(Dotfile.is_user_dotfile("./dotfiles-user"))
        self.assertFalse(Dotfile.is_user_dotfile("./dotfiles-team"))
