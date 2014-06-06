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
        self.assertEqual(r.dotfiles.files['inputrc'].aggregated_contents(),
                         "Space: magic-space\nset show-all-if-ambiguous on")
        self.assertEqual(r.dotfiles.files['sub/somerc'].aggregated_contents(),
                         "export EDITOR=vim\nHISTFILESIZE=100000000")
