import os


def _run_hook_if_exists(filename):
    if not os.path.exists(filename):
        return
    print "Running hook: {}".format(filename)
    os.system("./{}".format(filename))


def run_pre():
    return _run_hook_if_exists("dotbuild-pre.sh")


def run_post():
    return _run_hook_if_exists("dotbuild-post.sh")
