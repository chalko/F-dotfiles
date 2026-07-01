import unittest
import os
import shutil
import tempfile
import importlib.util

spec = importlib.util.spec_from_file_location("f_dotfiles", "f-dotfiles.py")
f_dotfiles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f_dotfiles)

class TestFDotfiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

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

if __name__ == "__main__":
    unittest.main()
