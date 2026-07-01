import os
import shutil
import tempfile
import unittest
import importlib.util

# Load the module dynamically since it has a hyphen in its name
spec = importlib.util.spec_from_file_location("f_dotfiles", "f-dotfiles.py")
f_dotfiles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f_dotfiles)

class TestFDotfiles(unittest.TestCase):
    def setUp(self):
        self.test_dir_safe = "test_dir_safe"
        os.makedirs(self.test_dir_safe, exist_ok=True)
        with open(os.path.join(self.test_dir_safe, "a.txt"), "w") as f:
            f.write("a")
        with open(os.path.join(self.test_dir_safe, "b.txt"), "w") as f:
            f.write("b")

        self.vuln_dir = "test_dir; echo 'VULNERABLE' > vuln.txt"
        os.makedirs(self.vuln_dir, exist_ok=True)
        with open(os.path.join(self.vuln_dir, "c.txt"), "w") as f:
            f.write("c")

        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_dir_safe):
            shutil.rmtree(self.test_dir_safe)
        if os.path.exists(self.vuln_dir):
            shutil.rmtree(self.vuln_dir)
        if os.path.exists("vuln.txt"):
            os.remove("vuln.txt")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_make_tree_safe_dir(self):
        tree = f_dotfiles.make_tree(self.test_dir_safe)
        self.assertIn("├── a.txt", tree)
        self.assertIn("└── b.txt", tree)

    def test_make_tree_vuln_dir(self):
        # Even with a semi-colon and echo in the dir name, it should not execute the command
        tree = f_dotfiles.make_tree(self.vuln_dir)

        # Check that tree was generated (safely resolving the path)
        self.assertIn("└── c.txt", tree)

        # Ensure the vulnerability wasn't exploited
        self.assertFalse(os.path.exists("vuln.txt"), "Command injection vulnerability exploited!")

    def test_extract_descriptions(self):
        file1 = os.path.join(self.test_dir, "test1.txt")
        with open(file1, "w") as f:
            f.write("# test1.txt: Description 1\nSome other text\n")

        file2 = os.path.join(self.test_dir, "test2.zsh")
        with open(file2, "w") as f:
            f.write("# test2.zsh: Description with dot\n")

        file3 = os.path.join(self.test_dir, "test3.txt")
        with open(file3, "w") as f:
            f.write("Line 1\nLine 2\n# test3.txt: Description line 3\n")

        # Test partial match (should NOT match)
        file4 = os.path.join(self.test_dir, "est4.txt")
        with open(file4, "w") as f:
            f.write("# test4.txt: This is for test4, not est4\n")

        desc = f_dotfiles.extract_descriptions(self.test_dir)
        base = os.path.basename(self.test_dir)

        self.assertEqual(desc.get(os.path.join(base, "test1.txt")), "Description 1")
        self.assertEqual(desc.get(os.path.join(base, "test2.zsh")), "Description with dot")
        self.assertEqual(desc.get(os.path.join(base, "test3.txt")), "Description line 3")
        self.assertIsNone(desc.get(os.path.join(base, "est4.txt")))

if __name__ == '__main__':
    unittest.main()
