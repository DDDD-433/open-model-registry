import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from registry import load_registry, memory_estimates
from validate_registry import validate


class RegistryTests(unittest.TestCase):
    def test_seed_registry_is_valid(self):
        data = load_registry()
        self.assertEqual(validate(data), [])

    def test_model_ids_are_unique(self):
        models = load_registry()["models"]
        self.assertEqual(len(models), len({model["model_id"] for model in models}))

    def test_memory_estimates_are_weight_only(self):
        self.assertEqual(memory_estimates(4), {"fp16": 8, "int8": 4, "int4": 2})


if __name__ == "__main__":
    unittest.main()
