"""Unit tests for human body volume calculation models.

These tests verify individual functions in isolation using pytest-style
assertions, parametrize, and fixtures.
"""

import inspect

import pytest

from human_body_volume import (
    format_proportions,
    get_bmi,
    get_bmi_body_fat_ratio,
    get_bmi_body_volume,
    get_bmi_category,
    get_body_density,
    get_brozek_body_fat_ratio,
    get_brozek_body_volume,
    get_cdda_original_volume,
    get_cdda_simple_brozek_volume,
    get_siri_body_fat_ratio,
    get_siri_body_volume,
    get_two_compartment_body_volume,
)

# ── Body density (four-compartment model) ─────────────────────────────────


class TestGetBodyDensity:
    """Tests for the four-compartment body density model."""

    @pytest.mark.parametrize("bf", [0.0, 0.05, 0.12, 0.20, 0.35, 0.50, 0.80, 1.0])
    def test_mass_fractions_sum_to_one(self, bf):
        """Mass fractions must always sum to 1.0."""
        result = get_body_density(bf)
        total = sum(result["proportions"].values())
        assert total == pytest.approx(1.0, abs=1e-10)

    def test_default_density(self):
        """Default (12 % fat) density should be close to literature ~1.07."""
        result = get_body_density()
        assert result["average_density"] == pytest.approx(1.075, abs=0.01)

    def test_ffm_density_near_standard(self):
        """Fat-free-mass density (BF=0) should be close to 1.1 kg/L."""
        result = get_body_density(0.0)
        assert result["average_density"] == pytest.approx(1.1, abs=0.01)

    def test_pure_fat_density(self):
        """Pure fat (BF=1) density should equal fat density (0.9 kg/L)."""
        result = get_body_density(1.0)
        assert result["average_density"] == pytest.approx(0.9, abs=1e-5)

    def test_density_decreases_with_fat(self):
        """Higher body fat should yield lower density."""
        d_low = get_body_density(0.10)["average_density"]
        d_high = get_body_density(0.40)["average_density"]
        assert d_low > d_high

    def test_clamps_negative_body_fat(self):
        """Negative body fat ratio should be clamped to 0."""
        result = get_body_density(-0.5)
        expected = get_body_density(0.0)["average_density"]
        assert result["average_density"] == pytest.approx(expected)

    def test_clamps_body_fat_above_one(self):
        """Body fat ratio above 1.0 should be clamped to 1.0."""
        result = get_body_density(1.5)
        expected = get_body_density(1.0)["average_density"]
        assert result["average_density"] == pytest.approx(expected)

    def test_mineral_compartment_present(self):
        """The mineral compartment should appear in the proportions."""
        result = get_body_density(0.12)
        assert "mineral" in result["proportions"]
        assert result["proportions"]["mineral"] > 0


# ── BMI helpers ────────────────────────────────────────────────────────────


class TestBMI:
    """Tests for BMI helper functions."""

    def test_bmi_70kg_175cm(self):
        """BMI for 70 kg / 1.75 m should be ~22.86."""
        assert get_bmi(1.75, 70) == pytest.approx(22.857, abs=0.01)

    @pytest.mark.parametrize(
        ("bmi", "expected"),
        [
            (22.0, "Normal"),
            (27.0, "Overweight"),
            (42.0, "Obese (Class III)"),
            (14.0, "Severe thinness"),
            (16.5, "Moderate thinness"),
            (17.5, "Mild thinness"),
            (31.0, "Obese (Class I)"),
            (36.0, "Obese (Class II)"),
        ],
    )
    def test_bmi_category(self, bmi, expected):
        assert get_bmi_category(bmi) == expected


# ── BMI → body-fat ratio ──────────────────────────────────────────────────


class TestBMIBodyFatRatio:
    """Tests for the Deurenberg BMI→body-fat conversion."""

    def test_male_30_bmi22(self):
        """30-year-old male with BMI 22 should have BF% in plausible range."""
        bfr = get_bmi_body_fat_ratio(22, "male", 30)
        assert 0.05 < bfr < 0.35

    def test_female_higher_fat_than_male(self):
        """Females should have higher estimated BF% than males at same BMI."""
        bfr_m = get_bmi_body_fat_ratio(25, "male", 30)
        bfr_f = get_bmi_body_fat_ratio(25, "female", 30)
        assert bfr_f > bfr_m


# ── Volume models – unit-level checks ─────────────────────────────────────


class TestVolumeModels:
    """Cross-model sanity checks."""

    def test_volume_positive_normal_case(self, normal_person):
        """All models should return positive volume for normal inputs."""
        h = normal_person["height"]
        w = normal_person["weight"]
        assert get_cdda_original_volume(h) > 0
        assert get_cdda_simple_brozek_volume(h, w) > 0
        assert get_bmi_body_volume(h, w)["volume"] > 0
        assert get_brozek_body_volume(h, w)["volume"] > 0
        assert get_siri_body_volume(h, w)["volume"] > 0
        assert get_two_compartment_body_volume(h, w) > 0

    def test_volume_within_plausible_range(self, normal_person):
        """For a 70 kg person, volume should be roughly 55–85 L."""
        h = normal_person["height"]
        w = normal_person["weight"]
        for vol in [
            get_bmi_body_volume(h, w)["volume"],
            get_brozek_body_volume(h, w)["volume"],
            get_siri_body_volume(h, w)["volume"],
            get_two_compartment_body_volume(h, w),
        ]:
            assert 55 < vol < 85, f"Volume {vol:.2f} outside plausible range"

    @pytest.mark.parametrize(
        ("h", "w"),
        [(1.75, 70), (1.62, 55), (1.80, 90)],
    )
    def test_two_compartment_close_to_bmi_model(self, h, w):
        """Two-compartment and BMI models should agree within ~5 %."""
        v_bmi = get_bmi_body_volume(h, w)["volume"]
        v_tc = get_two_compartment_body_volume(h, w)
        assert v_bmi == pytest.approx(v_tc, rel=0.05)

    def test_heavier_person_larger_volume(self):
        """Heavier person at same height should have larger volume."""
        h = 1.75
        v_light = get_two_compartment_body_volume(h, 60)
        v_heavy = get_two_compartment_body_volume(h, 100)
        assert v_heavy > v_light

    def test_cdda_original_independent_of_weight(self):
        """CDDA Original only depends on height, not weight."""
        vol_a = get_cdda_original_volume(1.75)
        vol_b = get_cdda_original_volume(1.75)
        assert vol_a == vol_b
        sig = inspect.signature(get_cdda_original_volume)
        assert list(sig.parameters.keys()) == ["height"]


# ── Brozek & Siri body-fat-from-density formulas ──────────────────────────


class TestBrozekSiriFormulas:
    """Tests for the Brozek and Siri body-fat-from-density formulas."""

    def test_brozek_standard_density(self):
        """Brozek at D=1.0 should give a well-defined BF ratio."""
        bfr = get_brozek_body_fat_ratio(1.0)
        assert bfr == pytest.approx(4.57 - 4.142, abs=1e-5)

    def test_siri_standard_density(self):
        """Siri at D=1.0 should give a well-defined BF ratio."""
        bfr = get_siri_body_fat_ratio(1.0)
        assert bfr == pytest.approx(4.95 - 4.50, abs=1e-5)


# ── Format proportions ────────────────────────────────────────────────────


class TestFormatProportions:
    """Tests for the proportion formatting helper."""

    def test_format_basic(self):
        """Formatting should produce uppercase initials with values."""
        result = format_proportions({"lipids": 0.12, "water": 0.65})
        assert "L:0.12" in result
        assert "W:0.65" in result
