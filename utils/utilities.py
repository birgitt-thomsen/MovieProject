""" Holds utility functions """


def color_text(text, color_code):
    """
    returns colored text based on color code
    """
    colors = {
        "ERROR": 31, #red
        "SUCCESS": 32, #green
        "WARN": 33,  # yellow
        "MENU": 34, #blue
        "INPUT": 35 #bold
    }
    code = colors.get(color_code, "MENU")
    return f"\033[{code}m{text}\033[0m"

def format_text(text, type):
    """
    returns bold text
    """
    types = {
        "INPUT": 1 #bold
    }
    code = types.get(type, "INPUT")
    return f"\033[{code}m{text}\033[0m"

# BLUE = "\033[34m"
# YELLOW = "\033[33m"
# GREEN = "\033[32m"
# RED = "\033[31m"
# BOLD = "\033[1m"
# RESET = "\033[0m"
