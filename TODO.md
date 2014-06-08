
figure out how to handle directories (rsync merge them?)
* actually, I think the best way to do this is to:
    * foreach directory, create it
    * foreach file in each directory, symlink it


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
