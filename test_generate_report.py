#!/usr/bin/env python3
"""Unit tests for the report generation script."""

import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from generate_report import (
    _volume_grid,
    _cdda_original_grid,
    generate_comparison_table,
    make_bmi_classification_map,
    make_heatmaps,
    make_humanoid_figures,
    make_line_plots,
    make_model_comparison,
    write_report_md,
)
from human_body_volume import (
    get_bmi_body_volume,
    get_cdda_original_volume,
)

import numpy as np


# Small weight/height arrays for fast tests
TEST_WEIGHTS = np.array([50, 70, 90])
TEST_HEIGHTS = np.array([1.60, 1.75, 1.90])


class TestVolumeGrid(unittest.TestCase):
    """Tests for the volume-grid helper functions."""

    def test_volume_grid_shape(self):
        """Grid shape should match (len(heights), len(weights))."""
        fn = lambda h, w: get_bmi_body_volume(h, w)
        grid = _volume_grid(fn, TEST_WEIGHTS, TEST_HEIGHTS)
        self.assertEqual(grid.shape, (3, 3))

    def test_volume_grid_positive(self):
        """All grid values should be positive for normal inputs."""
        fn = lambda h, w: get_bmi_body_volume(h, w)
        grid = _volume_grid(fn, TEST_WEIGHTS, TEST_HEIGHTS)
        self.assertTrue(np.all(grid > 0))

    def test_cdda_original_grid_rows_constant(self):
        """CDDA Original grid rows should be constant (no weight effect)."""
        grid = _cdda_original_grid(TEST_WEIGHTS, TEST_HEIGHTS)
        for row in grid:
            self.assertTrue(np.allclose(row, row[0]))

    def test_cdda_original_grid_shape(self):
        """CDDA Original grid shape should match inputs."""
        grid = _cdda_original_grid(TEST_WEIGHTS, TEST_HEIGHTS)
        self.assertEqual(grid.shape, (3, 3))


class TestFigureGeneration(unittest.TestCase):
    """Tests that figure-generation functions produce PNG files."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    @patch("generate_report.REPORT_DIR")
    def test_make_heatmaps_creates_file(self, mock_dir):
        mock_dir.__str__ = lambda s: self.tmpdir
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_heatmaps(TEST_WEIGHTS, TEST_HEIGHTS)
        self.assertTrue(os.path.isfile(path))
        self.assertGreater(os.path.getsize(path), 0)

    @patch("generate_report.REPORT_DIR")
    def test_make_line_plots_creates_file(self, mock_dir):
        mock_dir.__str__ = lambda s: self.tmpdir
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_line_plots(TEST_WEIGHTS, TEST_HEIGHTS)
        self.assertTrue(os.path.isfile(path))

    @patch("generate_report.REPORT_DIR")
    def test_make_bmi_classification_creates_file(self, mock_dir):
        mock_dir.__str__ = lambda s: self.tmpdir
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_bmi_classification_map(TEST_WEIGHTS, TEST_HEIGHTS)
        self.assertTrue(os.path.isfile(path))

    @patch("generate_report.REPORT_DIR")
    def test_make_humanoid_figures_creates_file(self, mock_dir):
        mock_dir.__str__ = lambda s: self.tmpdir
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_humanoid_figures()
        self.assertTrue(os.path.isfile(path))

    @patch("generate_report.REPORT_DIR")
    def test_make_model_comparison_creates_file(self, mock_dir):
        mock_dir.__str__ = lambda s: self.tmpdir
        with patch("generate_report.REPORT_DIR", self.tmpdir):
            path = make_model_comparison(TEST_WEIGHTS)
        self.assertTrue(os.path.isfile(path))


class TestComparisonTable(unittest.TestCase):
    """Tests for the Markdown table generator."""

    def test_table_contains_markdown_headers(self):
        """Output should contain Markdown table headers."""
        md = generate_comparison_table()
        self.assertIn("| Weight (kg)", md)
        self.assertIn("| BMI |", md)

    def test_table_contains_heights(self):
        """Output should mention the selected heights."""
        md = generate_comparison_table()
        self.assertIn("1.75", md)
        self.assertIn("2.00", md)

    def test_table_contains_categories(self):
        """Output should contain BMI category names."""
        md = generate_comparison_table()
        self.assertIn("Normal", md)


class TestWriteReportMd(unittest.TestCase):
    """Test for the Markdown report writer."""

    def test_write_report_md_creates_file(self):
        """write_report_md should create REPORT.md."""
        tmpfile = os.path.join(tempfile.mkdtemp(), "REPORT.md")
        with patch("generate_report.REPORT_MD", tmpfile):
            write_report_md("| test | table |")
        self.assertTrue(os.path.isfile(tmpfile))
        with open(tmpfile, encoding="utf-8") as fh:
            content = fh.read()
        self.assertIn("Body Volume Calculation", content)
        self.assertIn("| test | table |", content)
        os.unlink(tmpfile)


if __name__ == "__main__":
    unittest.main()
