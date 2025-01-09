"""
Test suite for the BS4Extractor and ResultParser classes.
Tests the extraction and parsing of art-related search results from HTML files,
including data structure validation, error handling, and end-to-end functionality.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path

from src.extractors.bs4_extractor import BS4Extractor
from src.parse import ResultParser
from src.main import main


@pytest.fixture
def test_html_path():
    """
    Fixture providing path to the main test HTML file containing Van Gogh paintings data.
    Returns absolute path to ensure consistent file location regardless of test execution directory.
    """
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "files" / "van-gogh-paintings.html")


@pytest.fixture
def empty_html_path():
    """
    Fixture providing path to an empty HTML file for testing edge cases.
    Used to verify extractor behavior with invalid/empty input.
    """
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "files" / "empty.html")


@pytest.fixture
def picasso_html_path():
    """
    Fixture providing path to alternative test data (Picasso paintings).
    Used for testing consistency across different input files.
    """
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "files" / "picasso-paintings.html")


def test_extractor_initialization(test_html_path):
    """Test basic initialization of the BS4Extractor class."""
    extractor = BS4Extractor(test_html_path)
    assert extractor.url == test_html_path


def test_extractor_data_structure(test_html_path):
    """
    Test the structure of extracted data to ensure it meets expected format.
    Verifies presence and types of required fields in the extraction results.
    """
    extractor = BS4Extractor(test_html_path)
    results = extractor.start()

    assert isinstance(results, list)
    assert len(results) > 0

    # Test first painting data structure
    first_painting = results[0]
    required_fields = ["title", "date", "link"]

    for field in required_fields:
        assert field in first_painting
        assert isinstance(first_painting[field], str)

    # Test that either thumbnail or preload_thumbnail exists and is a string
    assert "thumbnail" in first_painting or "preload_thumbnail" in first_painting
    if "thumbnail" in first_painting and first_painting["thumbnail"] is not None:
        assert isinstance(first_painting["thumbnail"], str)

    if (
        "preload_thumbnail" in first_painting
        and first_painting["preload_thumbnail"] is not None
    ):
        assert isinstance(first_painting["preload_thumbnail"], str)


def test_nonexistent_file():
    """
    Test error handling when attempting to process a non-existent file.
    Ensures appropriate exception is raised.
    """
    with pytest.raises(Exception):
        extractor = BS4Extractor("nonexistent.html")
        extractor.start()


def test_empty_html_extraction(empty_html_path):
    """
    Test behavior when processing an empty HTML file.
    Verifies that an empty result list is returned rather than throwing an error.
    """
    extractor = BS4Extractor(empty_html_path)
    results = extractor.start()

    assert isinstance(results, list)
    assert len(results) == 0


def test_full_extraction_pipeline(test_html_path):
    """
    Integration test for the complete extraction and parsing pipeline.
    Tests both extraction of raw data and subsequent parsing into final format.
    """
    extractor = BS4Extractor(test_html_path)
    results = extractor.start()

    assert len(results) > 0

    parser = ResultParser(test_html_path)
    cleaned_results = parser.parse(results)

    assert len(cleaned_results) == len(results)

    first_painting = cleaned_results[0]
    assert "title" in first_painting
    assert "extensions" in first_painting
    assert "image" in first_painting


def test_multiple_files_consistency(test_html_path, picasso_html_path):
    """
    Test consistency of data structure across different input files.
    Ensures extractor produces consistent output format regardless of input content.
    """
    van_gogh = BS4Extractor(test_html_path)
    picasso = BS4Extractor(picasso_html_path)

    van_gogh_results = van_gogh.start()
    picasso_results = picasso.start()

    assert len(van_gogh_results) > 0
    assert len(picasso_results) > 0

    required_fields = ["title", "date", "link"]
    for field in required_fields:
        assert field in van_gogh_results[0]
        assert field in picasso_results[0]


def test_data_extraction_validation(test_html_path):
    """
    Test quality and validity of extracted data.
    Verifies that extracted fields contain meaningful data and proper formatting.
    """
    extractor = BS4Extractor(test_html_path)
    results = extractor.start()

    for painting in results:
        # Title should not be empty
        assert painting["title"].strip() != ""

        # Link should be a valid URL format
        assert painting["link"].startswith(("http", "https", "/"))

        # At least one type of thumbnail should be present
        has_thumbnail = bool(painting.get("thumbnail")) or bool(
            painting.get("preload_thumbnail")
        )
        assert has_thumbnail


def test_results_uniqueness(test_html_path):
    """
    Test that extraction results don't contain duplicate entries.
    Converts results to JSON strings for comparison to ensure deep equality check.
    """
    extractor = BS4Extractor(test_html_path)
    results = extractor.start()

    result_strings = [json.dumps(r, sort_keys=True) for r in results]
    unique_results = set(result_strings)

    assert len(unique_results) == len(results)


def test_json_output_writing(test_html_path):
    """
    Integration test for JSON output functionality.
    Tests the complete pipeline from extraction to file writing using a temporary directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "test-output.json")

        main(test_html_path, output_path)

        assert os.path.exists(output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            results = json.load(f)

        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(item, dict) for item in results)

        required_fields = ["title", "extensions", "image"]
        for item in results:
            for field in required_fields:
                assert field in item
