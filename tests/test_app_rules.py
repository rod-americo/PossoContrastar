from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "app" / "server.py"

spec = importlib.util.spec_from_file_location("posso_contrastar_server", SERVER_PATH)
assert spec is not None
server = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(server)


class RenalFunctionTests(unittest.TestCase):
    def test_adult_ckd_epi_drives_threshold_bucket(self) -> None:
        result = server.renal_function(
            {
                "creatinine_mg_dl": 1.0,
                "age_years": 45,
                "sex": "female",
                "weight_kg": 70,
            }
        )

        self.assertEqual(result["egfr_method"], "CKD-EPI 2021 creatinina")
        self.assertAlmostEqual(result["egfr_ckd_epi_2021"], 70.8, places=1)
        self.assertAlmostEqual(result["crcl_cockcroft_gault_ml_min"], 78.5, places=1)
        self.assertEqual(result["egfr_bucket"], "normal")
        self.assertIn("Cockcroft-Gault", " ".join(result["notes"]))

    def test_pediatric_schwartz_used_when_adult_formula_not_applicable(self) -> None:
        result = server.renal_function(
            {
                "creatinine_mg_dl": 0.5,
                "age_years": 8,
                "sex": "male",
                "height_cm": 120,
            }
        )

        self.assertIsNone(result["egfr_ckd_epi_2021"])
        self.assertEqual(result["egfr_method"], "Bedside Schwartz")
        self.assertAlmostEqual(result["egfr_bedside_schwartz"], 98.4, places=1)
        self.assertEqual(result["egfr_bucket"], "normal")

    def test_missing_inputs_are_reported_without_bucket_guessing(self) -> None:
        result = server.renal_function({"creatinine_mg_dl": 1.2})

        self.assertIsNone(result["egfr_for_thresholds"])
        self.assertEqual(result["egfr_bucket"], "unknown")
        self.assertTrue(result["notes"])


class DecisionSupportTests(unittest.TestCase):
    def test_iodinated_first_pass_low_egfr_and_metformin_raise_attention(self) -> None:
        result = server.decision_support(
            {
                "contrast_class": "iodinated",
                "route": "ia_first_pass",
                "creatinine_mg_dl": 1.4,
                "age_years": 75,
                "sex": "female",
                "weight_kg": 60,
                "metformin": True,
            }
        )

        titles = {card["title"] for card in result["cards"]}
        self.assertEqual(result["level"], "high")
        self.assertIn("IA primeira passagem e TFGe < 45", titles)
        self.assertIn("Metformina", titles)
        self.assertIn("Hidratação profilática", titles)

    def test_gbca_group_i_in_renal_risk_stops_flow(self) -> None:
        result = server.decision_support(
            {
                "contrast_class": "gbca",
                "gbca_group": "group_i",
                "creatinine_mg_dl": 3.0,
                "age_years": 70,
                "sex": "male",
                "weight_kg": 80,
            }
        )

        self.assertEqual(result["level"], "stop")
        self.assertTrue(any(card["title"] == "MCBG Grupo I" for card in result["cards"]))


class CalculatorTests(unittest.TestCase):
    def test_interval_unknown_renal_function_uses_documented_conservative_fallback(self) -> None:
        result = server.interval_calculator(
            {
                "previous_class": "iodinated",
                "next_class": "gbca",
                "sample_type": "blood",
            }
        )

        self.assertEqual(result["egfr_bucket"], "moderate")
        self.assertIn("fallback conservador", result["note"])
        self.assertEqual(result["between_injections"]["minimum"], "16 horas")

    def test_pediatric_calculator_uses_weight_based_rules(self) -> None:
        result = server.pediatric_calculator({"weight_kg": 10, "catheter": "22G"})

        self.assertEqual(result["iodinated_volume_ml"], {"min": 10.0, "max": 20.0})
        self.assertEqual(result["gbca_dose_mmol"], 0.1)
        self.assertEqual(result["max_injection_rate"], "2,5 mL/s")

    def test_extravasation_high_risk_appends_surgical_evaluation(self) -> None:
        result = server.extravasation_support({"volume_ml": 200, "severe_signs": False})

        self.assertEqual(result["level"], "high")
        self.assertIn("Encaminhar para avaliação cirúrgica.", result["actions"])
        self.assertTrue(any("Documentar detalhadamente" in action for action in result["actions"]))


class RetrievalTests(unittest.TestCase):
    def test_retrieve_returns_local_corpus_citations(self) -> None:
        results = server.retrieve("metformina contraste iodado", limit=3)

        self.assertTrue(results)
        self.assertIn("file", results[0])
        self.assertIn("snippet", results[0])


if __name__ == "__main__":
    unittest.main()
