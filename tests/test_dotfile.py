from dotbuild.dotfile import Dotfile, DotfileMap
from . import TestCase


class DotfileTests(TestCase):
    def test_keyname(self):
        dirpath = [".vim", "bundle"]
        filename = "README"
        keyname = DotfileMap.keyname(dirpath, filename)
        self.assertEqual(keyname, ".vim/bundle/README")

    def test_extract_module_name(self):
        path = "./dotfiles-z/vim/bundle/ctrlp"
        module, dirpath = DotfileMap._parse_dirpath(path)
        self.assertEqual(module, "dotfiles-z")
        self.assertEqual(dirpath, ["vim", "bundle", "ctrlp"])

    def test_recognize_prefix(self):
        self.assertTrue(Dotfile.has_dotfiles_prefix("./dotfiles-user"))
        self.assertTrue(Dotfile.has_dotfiles_prefix("./dotfiles-team"))
        self.assertFalse(Dotfile.has_dotfiles_prefix("ndotfiles-user"))
        self.assertTrue(Dotfile.is_user_source("dotfiles-user"))
        self.assertFalse(Dotfile.is_user_source("dotfiles-team"))

    def test_aggregate(self):
        d = Dotfile("", "inputrc")
        d.add_contents_from_source("dotfiles-a", "1")
        d.add_contents_from_source("dotfiles-user", "3")
        d.add_contents_from_source("dotfiles-z", "2")
        self.assertEqual(d.aggregated_contents(), "1\n2\n3")

    def test_add_to_map(self):
        dm = DotfileMap()
        dm.add("./dotfiles-user/.vim", "README", "2")
        dm.add("./dotfiles-a/.vim", "README", "1")
        self.assertTrue(".vim/README" in dm.files)
        self.assertEqual(len(dm.files), 1)
        self.assertEqual(dm.files[".vim/README"].dirpath, [".vim"])
