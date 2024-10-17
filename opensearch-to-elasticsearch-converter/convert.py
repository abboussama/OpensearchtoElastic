import json
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import logging
from datetime import datetime
import argparse

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def select_opensearch_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select OpenSearch Rule JSON Files",
        filetypes=[("JSON files", "*.json")],
        defaultextension=".json"
    )
    return file_paths

def load_opensearch_rule(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in file {file_path}: {e}")
        raise

def handle_threshold(threshold):
    if "count" in threshold:
        field = threshold["count"].get("field", "")
        value = threshold["count"].get("value", 1)
        if field:
            aggs = {
                "unique_count": {
                    "cardinality": {"field": field}
                }
            }
            condition = {
                "script": {
                    "source": f"ctx.payload.aggregations.unique_count.value >= {value}",
                }
            }
            return condition, aggs
    elif "value" in threshold:
        value = threshold.get("value")
        condition = {
            "compare": {
                "ctx.payload.hits.total": {"gte": value}
            }
        }
        return condition, None
    return {}, None

def handle_action(action_name, action_content):
    if action_name == "email":
        return {
            "email": {
                "to": action_content.get("to", "alert@example.com"),
                "subject": action_content.get("subject", "Alert Triggered"),
                "body": {"text": action_content.get("body", "Alert condition has been met.")}
            }
        }
    elif action_name == "slack":
        return {
            "slack": {
                "message": {
                    "to": action_content.get("channel", "#alerts"),
                    "text": action_content.get("text", "Alert Triggered")
                }
            }
        }
    else:
        logging.warning(f"Unknown action type '{action_name}' encountered. Adding as-is.")
        return {action_name: action_content}

def convert_to_elasticsearch_rule(opensearch_rule):
    elasticsearch_rule = {
        "trigger": {
            "schedule": opensearch_rule.get("schedule", {"interval": "1m"})
        },
        "input": {
            "search": {
                "request": {
                    "indices": [opensearch_rule.get("index", "default_index")],
                    "query": opensearch_rule.get("query", {"match_all": {}})
                }
            }
        },
        "condition": {},
        "actions": {}
    }

    if "threshold" in opensearch_rule:
        condition, aggs = handle_threshold(opensearch_rule["threshold"])
        elasticsearch_rule["condition"] = condition
        if aggs:
            elasticsearch_rule["input"]["search"]["request"]["aggs"] = aggs

    if "alert" in opensearch_rule and "actions" in opensearch_rule["alert"]:
        for action_name, action_content in opensearch_rule["alert"]["actions"].items():
            try:
                action_entry = handle_action(action_name, action_content)
                elasticsearch_rule["actions"][f"{action_name}_action"] = action_entry
            except Exception as e:
                logging.error(f"Error processing action '{action_name}': {e}")

    expected_fields = {"schedule", "index", "query", "threshold", "alert", "rule_id", "name", "description", "enabled", "type"}
    for key, value in opensearch_rule.items():
        if key not in expected_fields:
            logging.warning(f"Unknown top-level field '{key}' encountered. Adding to the output as-is.")
            elasticsearch_rule[key] = value

    return elasticsearch_rule

def generate_output_file_path(opensearch_rule, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    rule_name = (
        opensearch_rule.get("rule_id") or
        opensearch_rule.get("name") or
        opensearch_rule.get("rule", {}).get("title") or
        "rule"
    )

    rule_name = "".join(c for c in rule_name if c.isalnum() or c in (' ', '_', '-')).rstrip()

    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    file_name = f"{rule_name}_{current_date}.json"
    output_file_path = os.path.join(output_dir, file_name)

    return output_file_path

def save_elasticsearch_rule(elasticsearch_rule, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(elasticsearch_rule, f, indent=2)
        logging.info(f"Elasticsearch rule saved to {output_file}")
    except IOError as e:
        logging.error(f"Error saving Elasticsearch rule to {output_file}: {e}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert OpenSearch rules to Elasticsearch rules.')
    parser.add_argument('files', metavar='FILE', nargs='*', help='OpenSearch rule JSON files to convert.')
    parser.add_argument('-o', '--output-dir', default='output', help='Directory to save Elasticsearch rules.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity.')
    parser.add_argument('--no-gui', action='store_true', help='Do not use GUI; use command-line arguments only.')

    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.files:
        opensearch_rule_files = args.files
    elif not args.no_gui:
        opensearch_rule_files = select_opensearch_files()
        if not opensearch_rule_files:
            messagebox.showerror("Error", "No files selected.")
            sys.exit(1)
    else:
        logging.error("No input files specified.")
        sys.exit(1)

    for file_path in opensearch_rule_files:
        try:
            opensearch_rule = load_opensearch_rule(file_path)
            elasticsearch_rule = convert_to_elasticsearch_rule(opensearch_rule)
            elasticsearch_rule_file = generate_output_file_path(opensearch_rule, args.output_dir)
            save_elasticsearch_rule(elasticsearch_rule, elasticsearch_rule_file)
        except Exception as e:
            logging.error(f"Failed to process file {file_path}: {e}")

    logging.info("Conversion completed.")
    if not args.no_gui:
        messagebox.showinfo("Success", f"Elasticsearch rules saved to the {args.output_dir} folder.")

if __name__ == "__main__":
    main()