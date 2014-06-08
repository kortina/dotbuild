from mock import patch
from StringIO import StringIO
from dotbuild.reader import Reader
from . import TestCase


class ReaderTests(TestCase):

    def test_read(self):
        r = Reader(".")
        with patch('os.walk', new=mock_walk):
            with patch('__builtin__.open', new=mock_open, create=True):
                r.read()
        self.assertEqual(r.dotfile_map['inputrc'].aggregated_contents(),
                         "Space: magic-space\nset show-all-if-ambiguous on")
        self.assertEqual(r.dotfile_map['sub/somerc'].aggregated_contents(),
                         "export EDITOR=vim\nHISTFILESIZE=100000000")


def mock_walk(*args, **kwargs):
    """Returns mocked walk (with followlinks=True) of directory that looks
       like:

        dotfiles-danny -> friends/danny/dotfiles-user
        dotfiles-user
            inputrc
            sub
                somerc
        dotfiles-z-team
            sub
                somerc
        friends
            danny
                dotfiles-user
                    inputrc

        example usage:

        with patch('os.walk', new=mock_walk):
            for f in os.walk('/'):
                print f
    """

    items = [('.', ['dotfiles-danny', 'dotfiles-user',
                    'dotfiles-z-team', 'friends'], []),
             ('./dotfiles-danny', [], ['inputrc']),
             ('./dotfiles-user', ['sub'], ['inputrc']),
             ('./dotfiles-user/sub', [], ['somerc']),
             ('./dotfiles-z-team', ['sub'], []),
             ('./dotfiles-z-team/sub', [], ['somerc']),
             ('./friends', ['danny'], []),
             ('./friends/danny', ['dotfiles-user'], []),
             ('./friends/danny/dotfiles-user', [], ['inputrc'])]
    return iter(items)


class ContextualStringIO(StringIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        return False


def mock_open(*args, **kwargs):
    mocked = {'./dotfiles-danny/inputrc': 'Space: magic-space',
              './dotfiles-user/sub/somerc': 'HISTFILESIZE=100000000',
              './dotfiles-user/inputrc': 'set show-all-if-ambiguous on',
              './dotfiles-z-team/sub/somerc': 'export EDITOR=vim'}
    return ContextualStringIO(mocked[args[0]])
