import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deobfuskit import deobfuscate

class DeobfusKitTests(unittest.TestCase):
    def test_restores_names_but_not_strings(self):
        original = "def greet_user(name):\n    label = 'name'\n    return label + name\n"
        mapping = {"_v000": "greet_user", "_v001": "name", "_v002": "label"}
        obfuscated = "def _v000(_v001):\n    _v002 = 'name'\n    return _v002 + _v001\n"
        restored = deobfuscate(obfuscated, mapping)
        self.assertIn("def greet_user(name)", restored)
        self.assertIn("'name'", restored)
        self.assertIn("label + name", restored)

if __name__ == "__main__":
    unittest.main()
