
import json
from bs4 import BeautifulSoup

from extractors.bs4_extractor import BS4Extractor

async def main():
    html_file_path = "files/picasso-paintings.html"

    extractor = BS4Extractor(html_file_path)
    extractor.start()


if __name__ == "__main__":
    main()
