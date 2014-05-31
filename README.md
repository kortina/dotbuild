# dotbuild

`dotbuild` makes managing dotfiles more standardized and modular.

## Installation

    pip install dotbuild
  
## Usage

Running `dotbuild` looks at all files in folders in the current directory with the prefix `dotfiles-`, concatenates files with the same name, places them in a `build` directory, and then creates symlinks in your home directory to the complied files.  Directories get merged `rsync` style.

NB: `dotbuild` always applies files in the special/default directory `dotfiles-user` last--these are meant to be your personalized dotfiles which get applied last and can override settings in shared/team directories.

## Example

Suppose you run `dotbuild` in your `~/dotfiles` directory with the contents:

    dotfiles-team-venmo-all
        inputrc
        vimrc
    dotfiles-team-venmo-web
        vim
            bundle
                ctrlp
        vimrc
    dotfiles-user
        vim
            bundle
                pep8
        inputrc
        vimrc
    some-other-folder
        some-other-file

In your `~/dotfiles` directory, `dotbuild` will create:

    build
        inputrc   # = cat dotfiles-team-venmo-all/inputrc dotfiles-user/inputrc
        vim
            bundle
                ctrlp
                pep8
        vimrc     # = cat dotfiles-team-venmo-all/vimrc dotfiles-team-venmo-web/vimrc dotfiles-user/vimrc
  
And the symlinks in your home directory:

    ~/.inputrc    =>  ~/dotfiles/build/inputrc
    ~/.vim      =>  ~/dotfiles/build/vim
    ~/.vimrc      =>  ~/dotfiles/build/vimrc


## Tips

We recommend the following strategy for managing your `dotfiles` repos:

* Maintan a project on your personal github containing all of your `dotfiles`.  
* Maintain `dotfiles-user` as a local folder in your github `dotfiles` project.
* Create github repos for your team dotfiles repo(s) and submodule into your own `dotfiles` project.
* Include a friend's `dotfiles-user` directory by submoduling their `dotfiles` repo and symlinking from your `dotfiles` root, eg, <br />`git submoudle add github.com/myfriend/dotfiles friends/myfriend && ln -s friends/myfriend/dotfiles-user dotfiles-myfriend`

## Options

    -n
    --no-confirm
                Skip confirming deletion of existing dotfiles that would be overwritten


## Pre and Post Hooks

Dotbuild can run custom pre and post build hooks you define in your `dotfiles` home as

    dotbuild-pre.sh  # dotbuild runs this before the build
    dotbuild-post.sh # dotbuild runs this after the build


## Contributing

Open up a pull request, making sure to add tests for any new functionality.
