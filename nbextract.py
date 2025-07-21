import json
import sys
import re
from pathlib import Path

def extract_notebook_content(notebook_path, output_path=None):
    """
    Extract just cell content and outputs in simple text format.
    
    Format:
    Cell 1: <cell content>
    Cell 1 Output: <output text>
    
    Cell 2: <cell content>
    Cell 2 Output: <output text>
    ...
    """
    
    # Read the notebook
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {notebook_path} is not a valid JSON file.")
        sys.exit(1)
    
    output_lines = []
    
    for i, cell in enumerate(notebook.get('cells', []), 1):
        # Extract cell content
        source = cell.get('source', [])
        if isinstance(source, list):
            cell_content = ''.join(source).strip()
        else:
            cell_content = str(source).strip()
        
        if cell_content:
            output_lines.append(f"Cell {i}: {cell_content}")
            
            # Extract outputs if they exist
            outputs = cell.get('outputs', [])
            if outputs:
                output_text = []
                
                for output in outputs:
                    # Handle different output types
                    if 'text' in output:
                        if isinstance(output['text'], list):
                            output_text.extend(output['text'])
                        else:
                            output_text.append(output['text'])
                    
                    elif 'data' in output:
                        data = output['data']
                        # Handle text/plain output
                        if 'text/plain' in data:
                            if isinstance(data['text/plain'], list):
                                output_text.extend(data['text/plain'])
                            else:
                                output_text.append(data['text/plain'])
                        
                        # Handle HTML output by stripping tags
                        elif 'text/html' in data:
                            html_content = data['text/html']
                            if isinstance(html_content, list):
                                html_content = ''.join(html_content)
                            # Simple HTML stripping - remove tags but keep content
                            clean_text = re.sub(r'<[^>]+>', '', html_content)
                            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                            if clean_text:
                                output_text.append(clean_text)
                    
                    # Handle stream output (like print statements)
                    elif output.get('output_type') == 'stream':
                        if isinstance(output.get('text', []), list):
                            output_text.extend(output['text'])
                        else:
                            output_text.append(output.get('text', ''))
                
                if output_text:
                    # Clean up the output text
                    clean_output = ''.join(output_text).strip()
                    # Remove ANSI escape codes
                    clean_output = re.sub(r'\x1b\[[0-9;]*m', '', clean_output)
                    if clean_output:
                        output_lines.append(f"Cell {i} Output: {clean_output}")
            
            output_lines.append("")  # Empty line between cells
    
    # Join all lines
    result = '\n'.join(output_lines)
    
    # Write to file or return
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Content extracted to {output_path}")
    else:
        print(result)
    
    return result

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Extract cell content and outputs from a Jupyter Notebook.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Example usage:
  python extract_jupyter_notebook.py my_notebook.ipynb
  python extract_jupyter_notebook.py my_notebook.ipynb -o extracted_content.txt
"""
    )
    parser.add_argument(
        "notebook_path",
        type=str,
        help="The path to the Jupyter Notebook file (.ipynb)."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        dest="output_path",
        default=None,
        help="The path to the output text file. If not provided, prints to console."
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.notebook_path)
    
    if not input_path.exists():
        print(f"Error: {input_path} not found")
        sys.exit(1)
    
    extract_notebook_content(input_path, args.output_path)

if __name__ == "__main__":
    main()

# Example usage:
# extract_notebook_content('notebook.ipynb', 'content.txt')  # Save to file
# extract_notebook_content('notebook.ipynb')  # Print to console