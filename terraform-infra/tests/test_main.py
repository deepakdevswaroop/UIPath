import unittest
import tempfile
import os
from main import update_tfvars

class TestUpdateTfvars(unittest.TestCase):
    def setUp(self):
        self.tfvars_path = tempfile.NamedTemporaryFile(delete=False).name

    def tearDown(self):
        os.remove(self.tfvars_path)

    def test_tfvars_update(self):
        sample_vars = {"vm_size": "Standard_B2s", "vm_count": "2"}
        update_tfvars(self.tfvars_path, sample_vars)

        with open(self.tfvars_path, "r") as file:
            content = file.read()
            self.assertIn('vm_size = "Standard_B2s"', content)
            self.assertIn('vm_count = 2', content)

if __name__ == '__main__':
    unittest.main()
