"""Integration tests for the report generation script.

These tests exercise the figure-generation and Markdown-writing pipeline,
verifying that each function produces the expected output files.  They use
a temporary directory so nothing is written to the real ``report/`` folder.
"""

import os
from unittest.mock import patch

import numpy as np
import pytest

from generate_report import (
    _cdda_original_grid,
    _volume_grid,
    generate_comparison_table,
    make_bmi_classification_map,
    make_heatmaps,
    make_humanoid_figures,
    make_line_plots,
    make_model_comparison,
    write_report_md,
)
from human_body_volume import get_bmi_body_volume

# ── Volume-grid helpers ────────────────────────────────────────────────────


class TestVolumeGrid:
    """Tests for the volume-grid helper functions."""

    def test_volume_grid_shape(self, test_weights, test_heights):
        """Grid shape should match (len(heights), len(weights))."""
        grid = _volume_grid(
            lambda h, w: get_bmi_body_volume(h, w), test_weights, test_heights
        )
        assert grid.shape == (3, 3)

    def test_volume_grid_positive(self, test_weights, test_heights):
        """All grid values should be positive for normal inputs."""
        grid = _volume_grid(
            lambda h, w: get_bmi_body_volume(h, w), test_weights, test_heights
        )
        assert np.all(grid > 0)

    def test_cdda_original_grid_rows_constant(self, test_weights, test_heights):
        """CDDA Original grid rows should be constant (no weight effect)."""
        grid = _cdda_original_grid(test_weights, test_heights)
        for row in grid:
            assert np.allclose(row, row[0])

    def test_cdda_original_grid_shape(self, test_weights, test_heights):
        """CDDA Original grid shape should match inputs."""
        grid = _cdda_original_grid(test_weights, test_heights)
        assert grid.shape == (3, 3)


# ── Figure generation (integration) ───────────────────────────────────────


class TestFigureGeneration:
    """Tests that figure-generation functions produce PNG files."""

    @pytest.fixture(autouse=True)
    def _tmpdir(self, tmp_path):
        self.tmpdir = str(tmp_path)

    def test_make_heatmaps_creates_file(self, test_weights, test_heights):
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_heatmaps(test_weights, test_heights)
        assert os.path.isfile(path)
        assert os.path.getsize(path) > 0

    def test_make_line_plots_creates_file(self, test_weights, test_heights):
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_line_plots(test_weights, test_heights)
        assert os.path.isfile(path)

    def test_make_bmi_classification_creates_file(self, test_weights, test_heights):
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_bmi_classification_map(test_weights, test_heights)
        assert os.path.isfile(path)

    def test_make_humanoid_figures_creates_file(self):
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_humanoid_figures()
        assert os.path.isfile(path)

    def test_make_model_comparison_creates_file(self, test_weights):
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_model_comparison(test_weights)
        assert os.path.isfile(path)


# ── Markdown table ─────────────────────────────────────────────────────────


class TestComparisonTable:
    """Tests for the Markdown table generator."""

    def test_table_contains_markdown_headers(self):
        md = generate_comparison_table()
        assert "| Weight (kg)" in md
        assert "| BMI |" in md

    def test_table_contains_heights(self):
        md = generate_comparison_table()
        assert "1.75" in md
        assert "2.00" in md

    def test_table_contains_categories(self):
        md = generate_comparison_table()
        assert "Normal" in md


# ── REPORT.md writer ──────────────────────────────────────────────────────


class TestWriteReportMd:
    """Test for the Markdown report writer."""

    def test_write_report_md_creates_file(self, tmp_path):
        tmpfile = str(tmp_path / "REPORT.md")
        with patch("generate_report.REPORT_MD", tmpfile):
            write_report_md("| test | table |")
        assert os.path.isfile(tmpfile)
        content = (tmp_path / "REPORT.md").read_text(encoding="utf-8")
        assert "Body Volume Calculation" in content
        assert "| test | table |" in content
