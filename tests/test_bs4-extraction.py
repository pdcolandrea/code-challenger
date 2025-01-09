import pytest
from pathlib import Path

from src.extractors.bs4_extractor import BS4Extractor


@pytest.fixture
def test_html_path():
    # Get the absolute path to the test files directory
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "files" / "van-gogh-paintings.html")


@pytest.fixture
def empty_html_path():
    # Get the absolute path to the empty test file
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "files" / "empty.html")


@pytest.fixture
def picasso_html_path():
    # Get the absolute path to another test file for comparison
    current_dir = Path(__file__).parent.parent
    return str(current_dir / "files" / "picasso-paintings.html")


def test_ai_extractor_initialization(test_html_path):
    extractor = BS4Extractor(test_html_path)
    assert extractor.url == test_html_path
