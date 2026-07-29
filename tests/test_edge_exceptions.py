import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_edge_exceptions import load_exceptions, validate


class EdgeExceptionTests(unittest.TestCase):
    def test_edge_exception_registry_is_valid(self):
        self.assertEqual(validate(load_exceptions()), [])

    def test_edge_exceptions_are_not_primary_models(self):
        exceptions = load_exceptions()["exceptions"]
        self.assertTrue(exceptions)
        self.assertTrue(all(item["total_parameters_b"] > 12 for item in exceptions))

    def test_active_parameter_trap_is_explicit(self):
        qwen = next(item for item in load_exceptions()["exceptions"] if item["model_id"] == "Qwen/Qwen3-30B-A3B")
        self.assertLess(qwen["active_parameters_b"], qwen["total_parameters_b"])
        self.assertEqual(qwen["reason"], "active-parameter-exception")


if __name__ == "__main__":
    unittest.main()
