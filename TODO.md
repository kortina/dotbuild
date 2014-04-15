
figure out how to handle directories (rsync merge them?)


Add these options

    --exclude
                dotbuild --exclude=team-venmo-web 
                would install all dotfiles in current directory *other than* `dotfiles-team-venmo-web`
                
                Accepts patterns, regex style, like --exclude=team.*
                
    --only
                dotbuild --only=team-venmo-all,team-venmo-web
                would ignore all dotfiles in current directory *other than* `dotfiles-team-venmo-all` and `dotfiles-team-venmo-web`
                NB: this would also exlclude the default direcotry, `dotfiles-user`
                
                Accepts patterns, regex style, like --exclude=team.*
                

Add hooks

## Pre and Post Hooks

Dotbuild can run custom pre and post build hooks you define in your `dotfiles` home as

    dotbuild-pre.sh  # dotbuild runs this before the build
    dotbuild-post.sh # dotbuild runs this after the build
