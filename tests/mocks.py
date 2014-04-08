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
    iterator = iter(items)
    yield iterator.next()
