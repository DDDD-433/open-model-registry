import sys
import unittest
from copy import deepcopy
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

    def test_exact_12b_boundary_is_valid(self):
        data = load_registry()
        boundary = deepcopy(data["models"][0])
        boundary["parameters"]["total_b"] = 12.0
        data["models"] = [boundary]
        self.assertEqual(validate(data), [])

    def test_effective_parameters_and_field_evidence_are_supported(self):
        models = load_registry()["models"]
        gemma = next(model for model in models if model["model_id"] == "google/gemma-4-E2B")
        self.assertLess(gemma["parameters"]["effective_b"], gemma["parameters"]["total_b"])
        self.assertIn("parameters", gemma["evidence"])

    def test_memory_estimates_are_weight_only(self):
        self.assertEqual(memory_estimates(4), {"fp16": 8, "int8": 4, "int4": 2})


if __name__ == "__main__":
    unittest.main()
