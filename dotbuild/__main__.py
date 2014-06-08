import logging
import sys

# If we are running from a wheel, add the wheel to sys.path
if __package__ in ('', None):
    import os
    # __file__ is dotbuild-*.whl/dotbuild/__main__.py
    # first dirname call strips of '/__main__.py',
    # second strips off '/dotbuild'
    # Resulting path is the name of the wheel itself
    # Add that to sys.path so we can import dotbuild
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)


from dotbuild.argparser import argparser
from dotbuild.reader import Reader
from dotbuild.writer import Writer
from dotbuild import hooks


def main():
    logging.basicConfig(level=logging.INFO)
    args = argparser.parse_args()
    confirm_overwrite = (args.no_confirm is False)
    hooks.run_pre()
    reader = Reader(".")
    reader.read()
    for dotfile in reader.dotfile_map.next_dotfile():
        writer = Writer(dirpath=dotfile.dirpath,
                        filename=dotfile.filename,
                        contents=dotfile.aggregated_contents(),
                        confirm_overwrite=confirm_overwrite)
        writer.write()
    hooks.run_post()

if __name__ == '__main__':
    main()
