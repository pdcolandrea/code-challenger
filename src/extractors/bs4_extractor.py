from bs4 import BeautifulSoup
import os.path

from extractors.element_selector import ElementSelector


class BS4Extractor:
    """
    A BeautifulSoup-based HTML extractor that parses feature mosiac from HTML files.
    This class handles the extraction of structured data from HTML mosiac components,
    including titles, dates, thumbnails, and related links.
    """

    def __init__(self, html_file_path: str) -> None:
        """
        Initialize the BS4Extractor with a path to an HTML file.

        Args:
            html_file_path (str): Path to the HTML file to parse. Must end with '.html'

        Raises:
            ValueError: If the file path is not a string or doesn't end with '.html'
            FileNotFoundError: If the specified HTML file does not exist
        """
        if not isinstance(html_file_path, str):
            raise ValueError("HTML file path must be a string ending in .html")

        if not os.path.isfile(html_file_path):
            raise FileNotFoundError(f"HTML file not found: {html_file_path}")

        # Read and parse the HTML content
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.url = html_file_path

    def start(self) -> list[dict]:
        """
        Begin the extraction process for all features in the mosiac.

        Returns:
            list: A list of dictionaries containing extracted feature data,
                 where each dictionary represents a mosiac item with its properties.
        """
        parsed_results = []

        # Get the root mosiac element and extract features
        mosiac_root = self.extract_root(self.soup)
        for feature in mosiac_root:
            parsed_results.append(self.extract_feature(feature))

        return parsed_results

    def extract_root(self, source: BeautifulSoup) -> list[BeautifulSoup]:
        """
        Extract the root mosiac element from the HTML.

        Args:
            source (BeautifulSoup): The BeautifulSoup object containing the parsed HTML

        Returns:
            list: A list of BeautifulSoup elements representing mosiac items
        """
        return source.select(ElementSelector.MOSIAC_ROOT)

    def extract_feature(self, source: BeautifulSoup) -> dict:
        """
        Extract all relevant data from a single mosiac feature element.

        Args:
            source (BeautifulSoup): A BeautifulSoup element representing a single mosiac item

        Returns:
            dict: A dictionary containing the extracted feature data with the following keys:
                - title: The feature's title text
                - date/extension: The feature's extension
                - thumbnail: The thumbnail image ID to be searched later in the Javascript
                - preload_thumbnail: The data-src attribute url for lazy loading
                - link: The feature's destination URL
        """
        feature = {}
        feature["title"] = source.select_one(ElementSelector.TITLE).getText(strip=True)
        feature["date"] = source.select_one(ElementSelector.DATE).getText(strip=True)
        feature["thumbnail"] = source.select_one(ElementSelector.THUMBNAIL).get("id")
        feature["preload_thumbnail"] = source.select_one(ElementSelector.THUMBNAIL).get(
            "data-src"
        )
        feature["link"] = source.select_one(ElementSelector.LINK).get("href")
        return feature
