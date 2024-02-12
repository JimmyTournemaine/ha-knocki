#!/usr/bin/env python3
# Convert mypy output to github annotation format (mypy do not handle this format)

import re
import sys

def format_mypy_error(file_path, line_number, message, error_type="error"):
    return f"::{error_type} file={file_path},line={line_number},endLine={line_number},title={message}::{message}"

def parse_mypy_output_from_file(file_path):
    with open(file_path, 'r') as file:
        mypy_output = file.read()
    return parse_mypy_output(mypy_output)

def parse_mypy_output(mypy_output):
    errors = []
    for line in mypy_output.splitlines():
        match = re.match(r'(?P<file_path>.*?):(?P<line_number>\d+): (?P<error_type>warning|error): (?P<message>.*)', line)
        if match:
            file_path = match.group('file_path')
            line_number = match.group('line_number')
            message = match.group('message')
            error_type = match.group('error_type')
            errors.append(format_mypy_error(file_path, line_number, message, error_type))
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mypy-report.py <mypy_output_file>")
        sys.exit(1)

    mypy_output_file = sys.argv[1]
    formatted_errors = parse_mypy_output_from_file(mypy_output_file)
    for error in formatted_errors:
        print(error)
