import argparse
argparser = argparse.ArgumentParser("python argparse_example.py")
argparser.add_argument('-n', '--no-confirm',
                       action='store_true', dest="no_confirm",
                       help="Skip confirming deletion of existing dotfiles " +
                       "that would be overwritten")


if __name__ == '__main__':
    args = argparser.parse_args()
    print args.no_confirm
