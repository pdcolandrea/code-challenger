
import json
from bs4 import BeautifulSoup

from extractors.bs4_extractor import BS4Extractor

async def main():
    html_file_path = "files/picasso-paintings.html"

    if not isinstance(html_file_path, str):
        raise ValueError("HTML file path must be a string")

    extractor = BS4Extractor(html_file_path)
    extractor.start()


if __name__ == "__main__":
    main()
