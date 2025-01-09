from bs4 import BeautifulSoup

from extractors.element_selector import ElementSelector

class BS4Extractor:
    """
    A BeautifulSoup-based HTML extractor that parses feature carousels from HTML files.
    This class handles the extraction of structured data from HTML carousel components,
    including titles, dates, thumbnails, and related links.
    """

    def __init__(self, html_file_path: str) -> None:
        """
        Initialize the BS4Extractor with a path to an HTML file.

        Args:
            html_file_path (str): Path to the HTML file to parse. Must end with '.html'

        Raises:
            ValueError: If the file path is not a string or doesn't end with '.html'
        """
        if not isinstance(html_file_path, str) or not html_file_path.endswith('.html'):
            raise ValueError("HTML file path must be a string ending in .html")
        
        # Read and parse the HTML content
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, "html.parser")
        self.url = html_file_path

    def start(self) -> list[dict]:
        """
        Begin the extraction process for all features in the carousel.
        
        Returns:
            list: A list of dictionaries containing extracted feature data,
                 where each dictionary represents a carousel item with its properties.
        """
        parsed_results = []

        # Get the root carousel element and extract features
        carousel_root = self.extract_root(self.soup)
        for feature in carousel_root:
            parsed_results.append(self.extract_feature(feature))

        return parsed_results
        
    def extract_root(self, source: BeautifulSoup) -> list[BeautifulSoup]:
        """
        Extract the root carousel element from the HTML.

        Args:
            source (BeautifulSoup): The BeautifulSoup object containing the parsed HTML

        Returns:
            list: A list of BeautifulSoup elements representing carousel items
        """
        return source.select(ElementSelector.CAROUSEL_ROOT)
    
    def extract_feature(self, source: BeautifulSoup) -> dict:
        """
        Extract all relevant data from a single carousel feature element.

        Args:
            source (BeautifulSoup): A BeautifulSoup element representing a single carousel item

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
        feature["preload_thumbnail"] = source.select_one(ElementSelector.THUMBNAIL).get("data-src")
        feature["link"] = source.select_one(ElementSelector.LINK).get("href")
        return feature