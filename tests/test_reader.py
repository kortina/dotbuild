from mock import patch
from dotbuild.reader import Reader
from . import TestCase
import mocks


class ReaderTests(TestCase):

    def test_read(self):
        r = Reader(".")
        with patch('os.walk', new=mocks.mock_walk):
            with patch('__builtin__.open', new=mocks.mock_open, create=True):
                r.read()
        self.assertEqual(r.dotfiles['inputrc'].dotfiles[0].dotfile_source,
                         "./dotfiles-danny")
        self.assertEqual(r.dotfiles['inputrc'].dotfiles[0].contents,
                         "Space: magic-space")
        self.assertEqual(r.dotfiles['bashrc'].dotfiles[0].dotfile_source,
                         "./dotfiles-z-team")
        self.assertEqual(r.dotfiles['inputrc'].user_dotfile.dotfile_source,
                         "./dotfiles-user")
        self.assertEqual(r.dotfiles['inputrc'].user_dotfile.contents,
                         "set show-all-if-ambiguous on")
