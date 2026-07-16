import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_variants import load_variants, validate


class VariantTests(unittest.TestCase):
    def test_variant_registry_is_valid(self):
        self.assertEqual(validate(load_variants()), [])

    def test_variants_keep_the_base_parameter_count(self):
        variants = load_variants()["variants"]
        bonsai_4b = next(item for item in variants if item["variant_id"] == "prism-ml/Bonsai-4B-mlx-1bit")
        self.assertEqual(bonsai_4b["total_parameters_b"], 4.0)
        self.assertLess(bonsai_4b["memory_estimate_gb"], 1.0)

    def test_over_limit_edge_exception_is_explicit(self):
        variants = load_variants()["variants"]
        bonsai_27b = next(item for item in variants if item["variant_id"] == "prism-ml/Bonsai-27B-mlx-1bit")
        self.assertEqual(bonsai_27b["parameter_scope"], "edge-exception")
        self.assertGreaterEqual(bonsai_27b["total_parameters_b"], 12.0)
        self.assertLessEqual(bonsai_27b["memory_estimate_gb"], 16.0)


if __name__ == "__main__":
    unittest.main()
