# Jupyter Notebook Content Extractor

This script extracts the cell content and outputs from a Jupyter Notebook (`.ipynb`) file and saves it to a text file or prints it to the console. This is useful for creating a smaller, more concise representation of a notebook, which can be easily shared or passed to a large language model (LLM) for inference.

## Features

- Extracts both code and markdown cells.
- Extracts cell outputs, including text, data, and stream outputs.
- Strips HTML tags from HTML outputs.
- Removes ANSI escape codes from outputs.
- Provides a simple and easy-to-read text format.
- Offers a command-line interface for easy use.

## Usage

To use the script, run it from the command line with the following arguments:

```bash
python nbextract.py <notebook.ipynb> [options]
```

### Arguments

- `notebook_path`: The path to the Jupyter Notebook file (`.ipynb`).

### Options

- `-o, --output <output_path>`: The path to the output text file. If not provided, the script will print the extracted content to the console.
- `-h, --help`: Show the help message and exit.

### Examples

To extract the content of a notebook and print it to the console:

```bash
python nbextract.py my_notebook.ipynb
```

To extract the content of a notebook and save it to a file named `extracted_content.txt`:

```bash
python nbextract.py my_notebook.ipynb -o extracted_content.txt
```

## Requirements

- Python 3.6+
- No external libraries are required.
