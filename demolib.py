import difflib

class Color:
    _WHITE = '\033[97m'
    _CYAN = '\033[96m'
    _MAGENTA = '\033[95m'
    _BLUE = '\033[94m'
    _YELLOW = '\033[93m'
    _GREEN = '\033[92m'
    _RED = '\033[91m'
    _BOLD = '\033[1m'
    _END = '\033[0m'
    _ITALIC = '\033[3m'

    @staticmethod
    def white(text, bold=False, italic=False):
        return Color._WHITE + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END
    
    @staticmethod
    def cyan(text, bold=False, italic=False):
        return Color._CYAN + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END
    
    @staticmethod
    def magenta(text, bold=False, italic=False):
        return Color._MAGENTA + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END
    
    @staticmethod
    def blue(text, bold=False, italic=False):
        return Color._BLUE + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END
    
    @staticmethod
    def yellow(text, bold=False, italic=False):
        return Color._YELLOW + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END
    
    @staticmethod
    def green(text, bold=False, italic=False):
        return Color._GREEN + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END
    
    @staticmethod
    def red(text, bold=False, italic=False):
        return Color._RED + (Color._BOLD if bold else '') + (Color._ITALIC if italic else '') + text + Color._END

    @staticmethod
    def bold(text):
        return Color._BOLD + text + Color._END

    @staticmethod
    def italic(text):
        return Color._ITALIC + text + Color._END

def numbered_code(code):
    code_lines = code.splitlines(True)
    code_with_lines = []
    for i, line in enumerate(code_lines):
        code_with_lines.append(str(i + 1) + ": " + line)
    return "".join(code_with_lines)

def apply_changes(code, changes: list):
    """
    Pass changes as loaded json (list of dicts)
    """
    original_code_lines = code.splitlines(True)

    # Filter out explanation elements
    operation_changes = [change for change in changes if "operation" in change]
    explanations = [
        change["explanation"] for change in changes if "explanation" in change
    ]

    # Sort the changes in reverse line order
    operation_changes.sort(key=lambda x: x["line"], reverse=True)

    code_lines = original_code_lines.copy()
    for change in operation_changes:
        operation = change["operation"]
        line = change["line"]
        content = change["content"]

        if operation == "Replace":
            code_lines[line - 1] = content + "\n"
        elif operation == "Delete":
            del code_lines[line - 1]
        elif operation == "InsertAfter":
            code_lines.insert(line, content + "\n")

    # Print explanations
    print(Color.blue("Explanations:", bold=True))
    for explanation in explanations:
        print(Color.blue(f"- {explanation}"))

    # Show the diff
    print(Color.cyan("\nChanges:", bold=True))
    diff = difflib.unified_diff(
        original_code_lines, code_lines, lineterm="")
    for line in diff:
        if line.startswith("+"):
            print(Color.green(line), end="")
        elif line.startswith("-"):
            print(Color.red(line), end="")
        else:
            print(line, end="")

    print(Color.white("\n##### Updated Code #####", bold=True))
    print("".join(code_lines))
