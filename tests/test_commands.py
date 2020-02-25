import unittest
import tempfile
from src.commands import *


class TestCommands(unittest.TestCase):
    def test_echo(self):
        self.assertEqual("a b c\n", echo(["a", "b", "c"]))

    def test_cat(self):
        file = tempfile.NamedTemporaryFile("w")
        file.write("abc\n123")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w")
        file2.write("def\n456")
        file2.flush()
        self.assertEqual("abc\n123def\n456", cat([file.name, file2.name]))
        file.close()
        file2.close()

    def test_wc(self):
        file = tempfile.NamedTemporaryFile("w")
        file.write("abc\n123")
        file.flush()
        file2 = tempfile.NamedTemporaryFile("w")
        file2.write("def\n456")
        file2.flush()
        self.assertEqual("2 2 7 " + file.name + "\n2 2 7 " + file2.name + "\n", wc([file.name, file2.name]))
        file.close()
        file2.close()

    def test_empty_cd(self):
        context = Context()
        cd([], context)
        self.assertEqual(os.path.expanduser("~") + "\n", pwd([], context))

    def test_incorrect_cd(self):
        with self.assertRaises(FileNotFoundError):
            cd(["abacaba"])
        with self.assertRaises(FileNotFoundError):
            cd(["README.md"])

    def test_cd(self):
        context = Context()
        with tempfile.TemporaryDirectory() as tmpdir:
            cd([tmpdir], context)
            self.assertEqual(tmpdir + "\n", pwd([], context))
            cd(["../" + os.path.basename(tmpdir)], context)
            self.assertEqual(tmpdir + "\n", pwd([], context))

    def test_cd_commands(self):
        context = Context()
        with tempfile.TemporaryDirectory() as tmpdir:
            cd([tmpdir], context)
            file = tempfile.NamedTemporaryFile("w", dir=tmpdir)
            file.write("abc\n123")
            file.flush()
            self.assertEqual("abc\n123", cat([file.name], context))
            self.assertEqual("2 2 7 " + file.name + "\n", wc([file.name], context))
            file.close()

    def test_ls(self):
        context = Context()
        self.assertEqual("test_commands.py\ntest_interpreter.py\ntest_parser.py", ls([], context))
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = tempfile.NamedTemporaryFile("w", dir=tmpdir)
            file2 = tempfile.NamedTemporaryFile("w", dir=tmpdir)
            expected = "\n".join(sorted([os.path.basename(file1.name), os.path.basename(file2.name)]))
            cd([tmpdir], context)
            self.assertEqual(expected, ls([], context))
            cd([".."], context)
            self.assertEqual(expected, ls([tmpdir], context))
