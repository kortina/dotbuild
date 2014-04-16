from StringIO import StringIO


def get_yes_input(*args, **kwargs):
    return "y"


def get_no_input(*args, **kwargs):
    return "n"


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


def mock_walk_dirs(*args, **kwargs):
    """Returns mocked walk (with followlinks=True) of directory that looks
       like:

        dotfiles-user
            vim
                bundle
                    pep8
                        README
        dotfiles-z
            vim
                bundle
                    ctrlp
                        README

        example usage:

        with patch('os.walk', new=mock_walk_dirs):
            for f in os.walk('.'):
                print f
    """

    items = [('.', ['dotfiles-user',
                    'dotfiles-z'], []),
             ('./dotfiles-user', ['vim'], []),
             ('./dotfiles-user/vim', ['bundle'], []),
             ('./dotfiles-user/vim/bundle', ['pep8'], []),
             ('./dotfiles-user/vim/bundle/pep8', [], ['README']),
             ('./dotfiles-z', ['vim'], []),
             ('./dotfiles-z/vim', ['bundle'], []),
             ('./dotfiles-z/vim/bundle', ['ctrlp'], []),
             ('./dotfiles-z/vim/bundle/ctrlp', [], ['README'])]
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
