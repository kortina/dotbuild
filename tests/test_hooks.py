import os
import stat
from dotbuild import hooks
from . import TestCase


class HookTests(TestCase):
    touchfile = "touchfile.txt"
    # following hookfile will simply create the above touchfile.txt
    hookfile = "dotbuild-pre.sh"

    def _remove_files(self):
        if os.path.exists(self.hookfile):
            os.remove(self.hookfile)
        if os.path.exists(self.touchfile):
            os.remove(self.touchfile)

    def setUp(self):
        self._remove_files()
        with open(self.hookfile, "w+") as f:
            f.write("touch {}".format(self.touchfile))
        # make sure the hook is executable:
        os.chmod(self.hookfile, stat.S_IXUSR | stat.S_IRUSR | stat.S_IWUSR)

    def tearDown(self):
        self._remove_files()

    def test_run_hook(self):
        self.assertFalse(os.path.exists(self.touchfile))
        hooks.run_pre()
        # make sure touchfile was created
        self.assertTrue(os.path.exists(self.touchfile))
