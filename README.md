# Extract Van Gogh Paintings Code Challenge

This is my Python implementation of the Van Gogh paintings extraction challenge. While the original challenge suggested Ruby, I've chosen Python due to my stronger experience with the language and its excellent web scraping ecosystem.

## Project Structure

```
.
├── files/                  # Challenge data files
│   ├── van-gogh-paintings.html
│   ├── picasso-paintings.html     # Verification dataset
│   ├── salvador-dali-paintings.html     # Verification dataset
│   ├── rembrandt-paintings.html     # Verification dataset
│   └── output/            # Extracted results
├── src/                   # Source code
│   ├── extractors/       # Extraction implementations
│   ├── main.py          # Entry point
│   └── parse.py         # Core parsing logic
├── tests/                # Test suite
└── requirements.txt      # Python dependencies
```

## Setup & Installation

1. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Running Extraction

```bash
# Run with default input (picasso-paintings.html)
python3 src/main.py

# Run with specific input file
python3 src/main.py --input files/van-gogh-paintings.html
```

Available arguments:

- `--input`: Path to the HTML file to process (default: files/picasso-paintings.html)

## Running Tests

```bash
pytest tests/
```

## Implementation Details

The extractor has been verified against multiple datasets:

1. Van Gogh paintings (primary dataset)
2. Picasso paintings (verification dataset)
3. Salvador Dali paintings (verification dataset)
4. Rembrandt paintings (verification dataset)

## Original Challenge Description

Goal is to extract a list of Van Gogh paintings from the attached Google search results page.

![Van Gogh paintings](https://github.com/serpapi/code-challenge/blob/master/files/van-gogh-paintings.png?raw=true "Van Gogh paintings")

### Challenge Requirements

- Extract painting `name`, `extensions` array (date), and Google `link` in an array
- Parse directly from the HTML result page ([html file]) in this repository
- No extra HTTP requests should be needed
- Include painting thumbnails present in the result page
- Test against 2 other similar result pages

[relevant test]: https://github.com/serpapi/test-knowledge-graph-desktop/blob/master/spec/knowledge_graph_claude_monet_paintings_spec.rb
[sample json]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/van-gogh-paintings.json
[html file]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/van-gogh-paintings.html
[expected array]: https://raw.githubusercontent.com/serpapi/code-challenge/master/files/expected-array.json
