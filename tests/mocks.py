from StringIO import StringIO


def mock_walk(*args, **kwargs):
    """Returns mocked walk (with followlinks=True) of directory that looks
       like:

        dotfiles-danny -> friends/danny/dotfiles-user
        dotfiles-user
            bashrc
            inputrc
        dotfiles-z-team
            bashrc
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
             ('./dotfiles-user', [], ['bashrc', 'inputrc']),
             ('./dotfiles-z-team', [], ['bashrc']),
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
              './dotfiles-user/bashrc': 'HISTFILESIZE=100000000',
              './dotfiles-user/inputrc': 'set show-all-if-ambiguous on',
              './dotfiles-z-team/bashrc': 'export EDITOR=vim'}
    return ContextualStringIO(mocked[args[0]])
