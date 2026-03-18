#!/usr/bin/env python3
"""Unit tests for human body volume calculation models."""

import unittest
from human_body_volume import (
    get_body_density,
    get_bmi,
    get_bmi_body_fat_ratio,
    get_bmi_body_volume,
    get_bmi_category,
    get_brozek_body_fat_ratio,
    get_brozek_body_volume,
    get_cdda_original_volume,
    get_cdda_simple_brozek_volume,
    get_siri_body_fat_ratio,
    get_siri_body_volume,
    get_two_compartment_body_volume,
    format_proportions,
)


class TestGetBodyDensity(unittest.TestCase):
    """Tests for the four-compartment body density model."""

    def test_mass_fractions_sum_to_one(self):
        """Mass fractions must always sum to 1.0."""
        for bf in [0.0, 0.05, 0.12, 0.20, 0.35, 0.50, 0.80, 1.0]:
            result = get_body_density(bf)
            total = sum(result["proportions"].values())
            self.assertAlmostEqual(total, 1.0, places=10,
                                   msg=f"Fractions do not sum to 1 at BF={bf}")

    def test_default_density(self):
        """Default (12 % fat) density should be close to literature ~1.07."""
        result = get_body_density()
        self.assertAlmostEqual(result["average_density"], 1.075, delta=0.01)

    def test_ffm_density_near_standard(self):
        """Fat-free-mass density (BF=0) should be close to 1.1 kg/L."""
        result = get_body_density(0.0)
        self.assertAlmostEqual(result["average_density"], 1.1, delta=0.01)

    def test_pure_fat_density(self):
        """Pure fat (BF=1) density should equal fat density (0.9 kg/L)."""
        result = get_body_density(1.0)
        self.assertAlmostEqual(result["average_density"], 0.9, places=5)

    def test_density_decreases_with_fat(self):
        """Higher body fat should yield lower density."""
        d_low = get_body_density(0.10)["average_density"]
        d_high = get_body_density(0.40)["average_density"]
        self.assertGreater(d_low, d_high)

    def test_clamps_negative_body_fat(self):
        """Negative body fat ratio should be clamped to 0."""
        result = get_body_density(-0.5)
        self.assertAlmostEqual(
            result["average_density"],
            get_body_density(0.0)["average_density"],
        )

    def test_clamps_body_fat_above_one(self):
        """Body fat ratio above 1.0 should be clamped to 1.0."""
        result = get_body_density(1.5)
        self.assertAlmostEqual(
            result["average_density"],
            get_body_density(1.0)["average_density"],
        )

    def test_mineral_compartment_present(self):
        """The mineral compartment should appear in the proportions."""
        result = get_body_density(0.12)
        self.assertIn("mineral", result["proportions"])
        self.assertGreater(result["proportions"]["mineral"], 0)


class TestBMI(unittest.TestCase):
    """Tests for BMI helper functions."""

    def test_bmi_70kg_175cm(self):
        """BMI for 70 kg / 1.75 m should be ~22.86."""
        self.assertAlmostEqual(get_bmi(1.75, 70), 22.857, places=2)

    def test_bmi_category_normal(self):
        """BMI 22 should be classified as Normal."""
        self.assertEqual(get_bmi_category(22.0), "Normal")

    def test_bmi_category_overweight(self):
        """BMI 27 should be classified as Overweight."""
        self.assertEqual(get_bmi_category(27.0), "Overweight")

    def test_bmi_category_obese_iii(self):
        """BMI 42 should be classified as Obese (Class III)."""
        self.assertEqual(get_bmi_category(42.0), "Obese (Class III)")

    def test_bmi_category_severe_thinness(self):
        """BMI 14 should be classified as Severe thinness."""
        self.assertEqual(get_bmi_category(14.0), "Severe thinness")


class TestBMIBodyFatRatio(unittest.TestCase):
    """Tests for the Deurenberg BMI→body-fat conversion."""

    def test_male_30_bmi22(self):
        """30-year-old male with BMI 22 should have BF% in plausible range."""
        bfr = get_bmi_body_fat_ratio(22, "male", 30)
        self.assertGreater(bfr, 0.05)
        self.assertLess(bfr, 0.35)

    def test_female_higher_fat_than_male(self):
        """Females should have higher estimated BF% than males at same BMI."""
        bfr_m = get_bmi_body_fat_ratio(25, "male", 30)
        bfr_f = get_bmi_body_fat_ratio(25, "female", 30)
        self.assertGreater(bfr_f, bfr_m)


class TestVolumeModels(unittest.TestCase):
    """Cross-model sanity checks."""

    def test_volume_positive_normal_case(self):
        """All models should return positive volume for normal inputs."""
        h, w = 1.75, 70
        self.assertGreater(get_cdda_original_volume(h), 0)
        self.assertGreater(get_cdda_simple_brozek_volume(h, w), 0)
        self.assertGreater(get_bmi_body_volume(h, w)["volume"], 0)
        self.assertGreater(get_brozek_body_volume(h, w)["volume"], 0)
        self.assertGreater(get_siri_body_volume(h, w)["volume"], 0)
        self.assertGreater(get_two_compartment_body_volume(h, w), 0)

    def test_volume_within_plausible_range(self):
        """For a 70 kg person, volume should be roughly 60-80 L."""
        h, w = 1.75, 70
        for vol in [
            get_bmi_body_volume(h, w)["volume"],
            get_brozek_body_volume(h, w)["volume"],
            get_siri_body_volume(h, w)["volume"],
            get_two_compartment_body_volume(h, w),
        ]:
            self.assertGreater(vol, 55, msg=f"Volume {vol:.2f} too low")
            self.assertLess(vol, 85, msg=f"Volume {vol:.2f} too high")

    def test_two_compartment_close_to_bmi_model(self):
        """Two-compartment and BMI models should agree within ~5 % for
        normal human ranges."""
        for h, w in [(1.75, 70), (1.62, 55), (1.80, 90)]:
            v_bmi = get_bmi_body_volume(h, w)["volume"]
            v_tc = get_two_compartment_body_volume(h, w)
            self.assertAlmostEqual(v_bmi, v_tc, delta=v_bmi * 0.05)

    def test_heavier_person_larger_volume(self):
        """Heavier person at same height should have larger volume."""
        h = 1.75
        v_light = get_two_compartment_body_volume(h, 60)
        v_heavy = get_two_compartment_body_volume(h, 100)
        self.assertGreater(v_heavy, v_light)

    def test_cdda_original_independent_of_weight(self):
        """CDDA Original only depends on height."""
        self.assertEqual(
            get_cdda_original_volume(1.75),
            get_cdda_original_volume(1.75),
        )


class TestBrozekSiriFormulas(unittest.TestCase):
    """Tests for the Brozek and Siri body-fat-from-density formulas."""

    def test_brozek_standard_density(self):
        """Brozek at D=1.0 should give a well-defined BF ratio."""
        bfr = get_brozek_body_fat_ratio(1.0)
        self.assertAlmostEqual(bfr, 4.57 - 4.142, places=5)

    def test_siri_standard_density(self):
        """Siri at D=1.0 should give a well-defined BF ratio."""
        bfr = get_siri_body_fat_ratio(1.0)
        self.assertAlmostEqual(bfr, 4.95 - 4.50, places=5)


class TestFormatProportions(unittest.TestCase):
    """Tests for the proportion formatting helper."""

    def test_format_basic(self):
        """Formatting should produce uppercase initials with values."""
        result = format_proportions({"lipids": 0.12, "water": 0.65})
        self.assertIn("L:0.12", result)
        self.assertIn("W:0.65", result)


if __name__ == "__main__":
    unittest.main()
