import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from discover_hf import category_guess, is_derivative, parameter_count_billions


class DiscoveryTests(unittest.TestCase):
    def test_parameter_count_uses_largest_weight_metadata_value(self):
        self.assertEqual(parameter_count_billions({"safetensors": {"parameters": {"BF16": 2_000_000_000}}}), 2.0)

    def test_parameter_count_prefers_total_metadata_for_mixed_models(self):
        self.assertEqual(
            parameter_count_billions(
                {"safetensors": {"parameters": {"BF16": 3_000_000_000}, "total": 4_250_000_000}}
            ),
            4.25,
        )

    def test_quantized_derivatives_are_excluded(self):
        self.assertTrue(is_derivative({"modelId": "example/model-GGUF", "tags": []}))

    def test_category_guess_prioritizes_ocr(self):
        self.assertEqual(category_guess({"pipeline_tag": "image-text-to-text", "tags": ["ocr"]}), "ocr-vision")


if __name__ == "__main__":
    unittest.main()
