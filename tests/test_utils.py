import tempfile
import unittest
from pathlib import Path

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.utils.label import Label


class LabelTests(unittest.TestCase):
    def test_classification_labels_ignore_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "labels.txt"
            path.write_text("cat\n\n dog \n", encoding="utf-8")
            labels = Label(str(path))
            labels.read_labels(CLASSIFICATION)
            self.assertEqual(labels.list, ["cat", "dog"])


if __name__ == "__main__":
    unittest.main()
