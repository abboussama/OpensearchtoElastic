
# OpenSearch to Elasticsearch Rule Converter

This script converts OpenSearch rule JSON files into Elasticsearch rule JSON files. It reads OpenSearch rules, processes them, and saves the converted rules in a specified output directory. The script supports both command-line and graphical user interface (GUI) modes, allowing flexibility in how you use it.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
  - [Graphical User Interface](#graphical-user-interface)
- [Options](#options)
- [Examples](#examples)
- [Logging](#logging)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Features

- Converts OpenSearch rule JSON files to Elasticsearch rule JSON files.
- Supports batch processing of multiple files.
- Handles various action types (email, Slack) and thresholds.
- Provides both command-line and GUI interfaces.
- Configurable output directory.
- Verbose logging for debugging and monitoring.

## Prerequisites

- **Python**: Version 3.6 or higher is required.
- **Required Python packages**:
  - `tkinter` (usually included with Python)
  - `argparse` (part of the standard library)
  - `logging` (part of the standard library)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/opensearch-to-elasticsearch-converter.git
   cd opensearch-to-elasticsearch-converter
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   - No additional packages need to be installed since all used modules are part of the Python Standard Library.
   - Ensure that tkinter is installed on your system:
     - For Debian/Ubuntu:
       ```bash
       sudo apt-get install python3-tk
       ```
     - For RedHat/CentOS:
       ```bash
       sudo yum install python3-tkinter
       ```

## Usage

The script can be used either through the command line or via a graphical user interface.

### Command-Line Interface

Run the script by specifying one or more OpenSearch rule JSON files as arguments:
```bash
python converter.py /path/to/rule1.json /path/to/rule2.json -o /path/to/output/dir
```

### Graphical User Interface

Simply run the script without any arguments:
```bash
python converter.py
```

## Options

- `FILE [FILE ...]`: One or more OpenSearch rule JSON files to convert.
- `-o, --output-dir OUTPUT_DIR`: Directory to save Elasticsearch rules (default: output).
- `-v, --verbose`: Increase output verbosity for debugging purposes.
- `--no-gui`: Do not use the GUI; use command-line arguments only.

## Examples

**Example 1: Convert Multiple Files with Verbose Output**
```bash
python converter.py rule1.json rule2.json -o converted_rules -v
```

**Example 2: Use GUI to Select Files**
```bash
python converter.py
```

**Example 3: Convert Files Without GUI**
```bash
python converter.py /path/to/rule.json --no-gui
```

## Logging

The script uses the logging module to provide informative messages about its operations. To enable verbose logging, use the `-v` or `--verbose` flag:
```bash
python converter.py rule.json -v
```

## Output

- Converted Elasticsearch rule files are saved in the specified output directory.
- Output files are named using the rule's rule_id, name, or title, followed by a timestamp.

## Contributing

Contributions are welcome! Please follow these steps:
1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit Your Changes**
   ```bash
   git commit -am 'Add some feature'
   ```
4. **Push to the Branch**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: Replace `yourusername` in the clone URL with your actual GitHub username, and ensure that the LICENSE file is included in your repository.

## Appendix: Detailed Functionality

### Script Breakdown
#### Main Functions

- `select_opensearch_files()`: Opens a file dialog to select OpenSearch rule JSON files.
- `load_opensearch_rule(file_path)`: Loads an OpenSearch rule from a JSON file.
- `convert_to_elasticsearch_rule(opensearch_rule)`: Converts an OpenSearch rule to an Elasticsearch rule.
- `handle_threshold(threshold)`: Processes threshold conditions for the Elasticsearch rule.
- `handle_action(action_name, action_content)`: Processes actions for the Elasticsearch rule.
- `generate_output_file_path(opensearch_rule, output_dir)`: Generates the output file path.
- `save_elasticsearch_rule(elasticsearch_rule, output_file)`: Saves the Elasticsearch rule to a JSON file.
- `parse_arguments()`: Parses command-line arguments.
- `main()`: The main function that orchestrates the conversion process.

### Supported Action Types

- **Email**: Converts OpenSearch email actions to Elasticsearch email actions.
- **Slack**: Converts OpenSearch Slack actions to Elasticsearch Slack actions.
- **Others**: Logs a warning and includes unknown action types as-is.

### Extensibility

The script is designed to be easily extensible:

- **Adding New Action Types**: Implement additional cases in the `handle_action` function.
- **Custom Thresholds**: Modify the `handle_threshold` function to support more complex conditions.
- **Logging Levels**: Adjust logging configurations as needed.

### Error Handling

- **File Operations**: Try-except blocks handle file-related errors, providing informative messages.
- **JSON Parsing**: Errors in parsing JSON files are caught and logged.
- **Action Processing**: Exceptions during action handling are caught, preventing the script from crashing.

### Best Practices

- **Virtual Environments**: Use virtual environments to manage dependencies.
- **Code Style**: The script follows PEP8 guidelines for readability.
- **Documentation**: Inline comments and docstrings provide context and explanations.
