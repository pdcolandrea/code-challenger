"""
Parser module for processing and transforming search results from HTML content.
Handles extraction and cleaning of various result attributes including titles, links, and images.
"""

import re

GOOGLE_URL = "https://www.google.com"

class ResultParser:
    """
    A parser class that processes HTML content and extracts structured information from search results.
    Handles the transformation of raw HTML data into a clean, consistent format.
    """

    def __init__(self, html_file_path: str):
        """
        Initialize the parser with the path to an HTML file.

        Args:
            html_file_path (str): Path to the HTML file containing search results
        """

        with open(html_file_path, "r", encoding="utf-8") as f:
            self.root_html_content = f.read()

    def parse(self, results: list[dict]) -> list[dict]:
        """
        Parse a list of raw search results into a standardized format.

        Args:
            results (list[dict]): List of raw search result dictionaries

        Returns:
            list[dict]: Processed results with cleaned and normalized data
        """
        result = []
        for item in results:
            features = {}

            # Clean and normalize the title text
            features["title"] = self.clean_text(item["title"])

            # Seems like some of the mosiac items don't have an extension
            if item.get("date"):
                features["extensions"] = [item.get("date")]
            else:
                features["extensions"] = []

            # Ensure links are absolute URLs
            if not item["link"].startswith("https://"):
                features["link"] = f"{GOOGLE_URL}{item['link']}"
            else:
                features["link"] = item["link"]

            # Extract image data if available
            # - If thumbnail is available, that means image should be available
            # - If not, the full URL used for lazy loading can be grabbed
            image = item.get("thumbnail")
            if image:
                features["image"] = self.extract_content(image)
            else:
                features["image"] = item.get("preload_thumbnail")

            result.append(features)
        return result

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Remove extra whitespace and normalize text.

        Args:
            text (str): Raw text to clean

        Returns:
            str: Cleaned text with normalized spacing
        """
        return " ".join(text.split())

    def extract_content(self, search_string: str) -> str:
        """
        Extract image content from HTML using regex patterns.
        Attempts to find base64 encoded image data associated with a search string.

        Args:
            search_string (str): Identifier to search for in the HTML content

        Returns:
            str|None: Base64 encoded image data if found, None otherwise
        """
        # Primary search: Look for image ID in JavaScript array
        pattern = f"ii=\\['{search_string}'\\][^']*?'(data:image[^']*)';"
        match = re.search(pattern, self.root_html_content)

        if match:
            return match.group(1)

        # Fallback search: Look for direct base64 assignment
        pattern = f"var s='(data:image[^']*)'.*?ii=\\['{search_string}'\\]"
        match = re.search(pattern, self.root_html_content)
        if match:
            return match.group(1)

        return None
