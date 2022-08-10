import sys
import os
import re
import ast


error_codes = {"S001": "Too long line",
               "S002": "Indentation is not a multiple of four",
               "S003": "Unnecessary semicolon",
               "S004": "At least two spaces required before inline comments",
               "S005": "TODO found",
               "S006": "More than two blank lines used before this line",
               "S007": "Too many spaces after construction_name",
               "S008": "Class name class_name should be written in CamelCase",
               "S009": "Function name function_name should be written in snake_case"}


def check_procedure(file_name):
    with open(file_name, 'r') as file:
        line_number = 1
        for line in file.readlines():
            check_length(line, line_number)
            check_indentation(line, line_number)
            check_semicolon(line, line_number)
            check_inline_comment(line, line_number)
            check_todo(line, line_number)
            check_blanks(line, line_number)
            check_spaces(line, line_number)
            check_class_name(line, line_number)
            check_function_name(file_name, line_number)
            check_argument_name(file_name, line_number)
            check_variable_name(file_name, line_number)
            check_mutable_default(file_name, line_number)
            line_number += 1


def check_length(current_line, current_line_number):
    if len(current_line) > 79:
        print(f'{path}: Line {current_line_number}: S001 {error_codes.get("S001")}')


def check_indentation(current_line, current_line_number):
    if current_line.startswith(" ") and not current_line.isspace():
        if (len(current_line) - len(current_line.lstrip())) % 4 != 0:
            print(f'{path}: Line {current_line_number}: S002 {error_codes.get("S002")}')


def check_semicolon(current_line, current_line_number):
    if ';' in current_line:
        if current_line[:current_line.index(';')].count("'") % 2 == 0 \
                and '#' not in current_line[:current_line.index(';')]:
            print(f'{path}: Line {current_line_number}: S003 {error_codes.get("S003")}')


def check_inline_comment(current_line, current_line_number):
    if "#" in current_line and not current_line.startswith("#"):
        if not current_line[current_line.index("#") - 2:].startswith("  "):
            print(f'{path}: Line {current_line_number}: S004 {error_codes.get("S004")}')


def check_todo(current_line, current_line_number):
    if "#" in current_line:
        if "todo" in current_line.lower():
            print(f'{path}: Line {current_line_number}: S005 {error_codes.get("S005")}')


def check_blanks(current_line, current_line_number):
    global blank_count
    if blank_count > 2 and not current_line.isspace():
        print(f'{path}: Line {current_line_number}: S006 {error_codes.get("S006")}')
        blank_count = 0
    else:
        if current_line.isspace():
            blank_count += 1
        else:
            blank_count = 0


def check_spaces(current_line, current_line_number):
    if not re.match(r'\s*def', current_line) and not re.match(r'^class', current_line):
        return
    if re.match(r"^class {2,}", current_line):
        print(f"{path}: Line {current_line_number}: S007 {error_codes.get('S007')} 'class'")
    elif re.match(r"\s*def {2,}", current_line):
        print(f"{path}: Line {current_line_number}: S007 {error_codes.get('S007')} 'def'")


def check_class_name(current_line, current_line_number):
    if not re.match(r'^class', current_line):
        return
    class_name = re.search(r'\s\b[\w]*[^:()]', current_line).group().lstrip()
    if class_name:
        if re.match(r'^\b[a-z].+', class_name) or re.match(r'^\b[a-z\d]+_.+', class_name):
            print(f"{path}: Line {current_line_number}: S008 Class name"
                  f" '{class_name}' should be written in CamelCase")


def check_function_name(current_file, current_line_number):
    tree = ast.parse(open(current_file).read())
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            if (re.match(r'^\b[A-Z].+', n.name) or re.match(r'^\b[a-z\d]+[A-Z].+', n.name)) \
                    and current_line_number == n.lineno:
                print(f"{path}: Line {current_line_number}: S009 '{n.name}' should be written in snake_case")


def check_argument_name(current_file, current_line_number):
    tree = ast.parse(open(current_file).read())
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            for arg in n.args.args:
                if (re.match(r'^\b[A-Z].+', arg.arg) or re.match(r'^\b[a-z\d]+[A-Z].+', arg.arg)) \
                        and current_line_number == n.lineno:
                    print(f"{path}: Line {current_line_number}: S010 '{arg.arg}' should be written in snake_case")


def check_variable_name(current_file, current_line_number):
    tree = ast.parse(open(current_file).read())
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign):
            for var in n.targets:
                if isinstance(var, ast.Name):
                    if (re.match(r'^\b[A-Z].+', var.id) or re.match(r'^\b[a-z\d]+[A-Z].+', var.id)) \
                            and current_line_number == var.lineno:
                        print(f"{path}: Line {current_line_number}: S011 '{var.id}' should be written in snake_case")
                elif isinstance(var, ast.Attribute):
                    if (re.match(r'^\b[A-Z].+', var.attr) or re.match(r'^\b[a-z\d]+[A-Z].+', var.attr)) \
                            and current_line_number == var.lineno:
                        print(f"{path}: Line {current_line_number}: S011 '{var.attr}' should be written in snake_case")


def check_mutable_default(current_file, current_line_number):
    tree = ast.parse(open(current_file).read())
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef):
            for arg in n.args.defaults:
                if (isinstance(arg, ast.List) or isinstance(arg, ast.Set) or isinstance(arg, ast.Dict)) \
                        and current_line_number == arg.lineno:
                    print(f"{path}: Line {current_line_number}: S012 '{n.args.args}' should be written in snake_case")


blank_count = 0
path = ""

if os.path.isfile(sys.argv[1]):
    path = sys.argv[1]
    check_procedure(sys.argv[1])
elif os.path.isdir(sys.argv[1]):
    entries = os.listdir(sys.argv[1])
    entries.sort()
    for entry in entries:
        if entry.endswith(".py"):
            path = sys.argv[1] + "/" + entry
            check_procedure(path)
