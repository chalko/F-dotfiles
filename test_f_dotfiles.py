import os
import shutil
import unittest
import importlib.util

# Load the module dynamically since it has a hyphen in its name
spec = importlib.util.spec_from_file_location("f_dotfiles", "f-dotfiles.py")
f_dotfiles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f_dotfiles)

class TestFDotfiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_dir_safe"
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "a.txt"), "w") as f:
            f.write("a")
        with open(os.path.join(self.test_dir, "b.txt"), "w") as f:
            f.write("b")

        self.vuln_dir = "test_dir; echo 'VULNERABLE' > vuln.txt"
        os.makedirs(self.vuln_dir, exist_ok=True)
        with open(os.path.join(self.vuln_dir, "c.txt"), "w") as f:
            f.write("c")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.vuln_dir):
            shutil.rmtree(self.vuln_dir)
        if os.path.exists("vuln.txt"):
            os.remove("vuln.txt")

    def test_make_tree_safe_dir(self):
        tree = f_dotfiles.make_tree(self.test_dir)
        self.assertIn("├── a.txt", tree)
        self.assertIn("└── b.txt", tree)

    def test_make_tree_vuln_dir(self):
        # Even with a semi-colon and echo in the dir name, it should not execute the command
        tree = f_dotfiles.make_tree(self.vuln_dir)

        # Check that tree was generated (safely resolving the path)
        self.assertIn("└── c.txt", tree)

        # Ensure the vulnerability wasn't exploited
        self.assertFalse(os.path.exists("vuln.txt"), "Command injection vulnerability exploited!")

if __name__ == '__main__':
    unittest.main()
