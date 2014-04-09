from mock import patch
from dotbuild.reader import Reader
from . import TestCase
import mocks


class ReaderTests(TestCase):
    def test_recognize_prefix(self):
        reader = Reader(".")
        self.assertTrue(reader._dir_has_dotfiles_prefix("./dotfiles-user"))
        self.assertTrue(reader._dir_has_dotfiles_prefix("./dotfiles-team"))
        self.assertFalse(reader._dir_has_dotfiles_prefix("ndotfiles-user"))
        self.assertTrue(reader._dir_is_user_dotfiles("./dotfiles-user"))
        self.assertFalse(reader._dir_is_user_dotfiles("./dotfiles-team"))

    def test_file_map(self):
        r = Reader(".")
        with patch('os.walk', new=mocks.mock_walk):
            with patch('__builtin__.open', new=mocks.mock_open, create=True):
                r._file_map()
        self.assertEqual(r.file_map['inputrc'][r.MODULES][0][r.NAME],
                         "./dotfiles-danny")
        self.assertEqual(r.file_map['inputrc'][r.MODULES][0][r.CONTENTS],
                         "Space: magic-space")
        self.assertEqual(r.file_map['bashrc'][r.MODULES][0][r.NAME],
                         "./dotfiles-z-team")
        self.assertEqual(r.file_map['inputrc'][r.USER][r.NAME],
                         "./dotfiles-user")
        self.assertEqual(r.file_map['inputrc'][r.USER][r.CONTENTS],
                         "set show-all-if-ambiguous on")
