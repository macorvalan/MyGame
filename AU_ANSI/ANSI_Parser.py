"""
ANSI - Color to ANSI Art screens used by Arkham Unknown

Use the funcion au_ansi_parser(screen) to parse a ANSI Art
screen create/modified with AU_ANSI Generator 2/TheDraw/Moebious

    Ex:
        parsed_screen = au_ansi_parser(ANSI_screen)

        parsed_screen:  string with the screen parsed to
                        evennia color tags

        ANSI_screen:    string with AU_ANSI color codes

This is best used when you e¿want to show a large ANSI
screen to the user.

This function do not conflict with the module ansi.py
"""

import re

# ANSI/EVENNIA Definitions

# Basic
AU_ANSI_BEEP = '\07'
AU_ANSI_ESCAPE = '\033'
AU_ANSI_ESCAPE_COLOR = '\033['
AU_ANSI_NORMAL = '\033[0M'

EVENNIA_ANSI_NORMAL = '|n'
EVENNIA_ANSI_LO = '|H'
EVENNIA_ANSI_HI = '|h'

# Blink
AU_ANSI_BLINK_ON = '\033[5m'
AU_ANSI_BLINK_LO = '\033[0;5m'
AU_ANSI_BLINK_HI = '\033[1;5m'

EVENNIA_ANSI_BLINK_ON = '|^'
EVENNIA_ANSI_BLINK_LO = '|^|H'
EVENNIA_ANSI_BLINK_HI = '|^|h'
EVENNIA_ANSI_UNDERLINE = '|u'

# Foreground colors
AU_ANSI_FORE_BLACK = '\033[30m'
AU_ANSI_FORE_RED = '\033[31m'
AU_ANSI_FORE_GREEN = '\033[32m'
AU_ANSI_FORE_YELLOW = '\033[33m'
AU_ANSI_FORE_BLUE = '\033[34m'
AU_ANSI_FORE_MAGENTA = '\033[35m'
AU_ANSI_FORE_CYAN = '\033[36m'
AU_ANSI_FORE_WHITE = '\033[37m'

# LO
EVENNIA_ANSI_FORE_LO_BLACK = '|x'
EVENNIA_ANSI_FORE_LO_RED = '|R'
EVENNIA_ANSI_FORE_LO_GREEN = '|G'
EVENNIA_ANSI_FORE_LO_YELLOW = '|Y'
EVENNIA_ANSI_FORE_LO_BLUE = '|B'
EVENNIA_ANSI_FORE_LO_MAGENTA = '|M'
EVENNIA_ANSI_FORE_LO_CYAN = '|C'
EVENNIA_ANSI_FORE_LO_WHITE = '|W'

# HI
EVENNIA_ANSI_FORE_HI_BLACK = '|x'
EVENNIA_ANSI_FORE_HI_RED = '|r'
EVENNIA_ANSI_FORE_HI_GREEN = '|g'
EVENNIA_ANSI_FORE_HI_YELLOW = '|y'
EVENNIA_ANSI_FORE_HI_BLUE = '|b'
EVENNIA_ANSI_FORE_HI_MAGENTA = '|m'
EVENNIA_ANSI_FORE_HI_CYAN = '|c'
EVENNIA_ANSI_FORE_HI_WHITE = '|w'

# Background colors
AU_ANSI_BACK_BLACK = '\033[40m'
AU_ANSI_BACK_RED = '\033[41m'
AU_ANSI_BACK_GREEN = '\033[42m'
AU_ANSI_BACK_YELLOW = '\033[43m'
AU_ANSI_BACK_BLUE = '\033[44m'
AU_ANSI_BACK_MAGENTA = '\033[45m'
AU_ANSI_BACK_CYAN = '\033[46m'
AU_ANSI_BACK_WHITE = '\033[47m'

# LO
EVENNIA_ANSI_BACK_LO_BLACK = '|[X'
EVENNIA_ANSI_BACK_LO_RED = '|[R'
EVENNIA_ANSI_BACK_LO_GREEN = '|[G'
EVENNIA_ANSI_BACK_LO_YELLOW = '|[Y'
EVENNIA_ANSI_BACK_LO_BLUE = '|[B'
EVENNIA_ANSI_BACK_LO_MAGENTA = '|[M'
EVENNIA_ANSI_BACK_LO_CYAN = '|[C'
EVENNIA_ANSI_BACK_LO_WHITE = '|[W'

# HI
EVENNIA_ANSI_BACK_HI_BLACK = '|[x'
EVENNIA_ANSI_BACK_HI_RED = '|[r'
EVENNIA_ANSI_BACK_HI_GREEN = '|[g'
EVENNIA_ANSI_BACK_HI_YELLOW = '|[y'
EVENNIA_ANSI_BACK_HI_BLUE = '|[b'
EVENNIA_ANSI_BACK_HI_MAGENTA = '|[m'
EVENNIA_ANSI_BACK_HI_CYAN = '|[c'
EVENNIA_ANSI_BACK_HI_WHITE = '|[w'

# TheDraw spacific codes
AU_ANSI_THEDRAW_START = '\033[?7h'
AU_ANSI_THEDRAW_FIRST = '\033[255D'
AU_ANSI_THEDRAW_END = '\033[0m\033[255D'

# Mapping ANSI<->EVENNIA
ansi_map = [
    ('0', EVENNIA_ANSI_NORMAL),
    ('0h', EVENNIA_ANSI_NORMAL),
    ('1', EVENNIA_ANSI_HI),
    ('4', EVENNIA_ANSI_UNDERLINE),
    ('5', EVENNIA_ANSI_BLINK_ON),
    ('30', EVENNIA_ANSI_FORE_LO_BLACK),
    ('31', EVENNIA_ANSI_FORE_LO_RED),
    ('32', EVENNIA_ANSI_FORE_LO_GREEN),
    ('33', EVENNIA_ANSI_FORE_LO_YELLOW),
    ('34', EVENNIA_ANSI_FORE_LO_BLUE),
    ('35', EVENNIA_ANSI_FORE_LO_MAGENTA),
    ('36', EVENNIA_ANSI_FORE_LO_CYAN),
    ('37', EVENNIA_ANSI_FORE_LO_WHITE),
    ('30h', EVENNIA_ANSI_FORE_HI_BLACK),
    ('31h', EVENNIA_ANSI_FORE_HI_RED),
    ('32h', EVENNIA_ANSI_FORE_HI_GREEN),
    ('33h', EVENNIA_ANSI_FORE_HI_YELLOW),
    ('34h', EVENNIA_ANSI_FORE_HI_BLUE),
    ('35h', EVENNIA_ANSI_FORE_HI_MAGENTA),
    ('36h', EVENNIA_ANSI_FORE_HI_CYAN),
    ('37h', EVENNIA_ANSI_FORE_HI_WHITE),
    ('40', EVENNIA_ANSI_BACK_LO_BLACK),
    ('41', EVENNIA_ANSI_BACK_LO_RED),
    ('42', EVENNIA_ANSI_BACK_LO_GREEN),
    ('43', EVENNIA_ANSI_BACK_LO_YELLOW),
    ('44', EVENNIA_ANSI_BACK_LO_BLUE),
    ('45', EVENNIA_ANSI_BACK_LO_MAGENTA),
    ('46', EVENNIA_ANSI_BACK_LO_CYAN),
    ('47', EVENNIA_ANSI_BACK_LO_WHITE),
    ('40h', EVENNIA_ANSI_BACK_HI_BLACK),
    ('41h', EVENNIA_ANSI_BACK_HI_RED),
    ('42h', EVENNIA_ANSI_BACK_HI_GREEN),
    ('43h', EVENNIA_ANSI_BACK_HI_YELLOW),
    ('44h', EVENNIA_ANSI_BACK_HI_BLUE),
    ('45h', EVENNIA_ANSI_BACK_HI_MAGENTA),
    ('46h', EVENNIA_ANSI_BACK_HI_CYAN),
    ('47h', EVENNIA_ANSI_BACK_HI_WHITE)
]

# LAst parsed escape command
LAST_EC_PARSED = '0'


# Parse funcion
def au_ansi_parser(ansi_screen):
    """
    Main function, start the parsing.
    """
    parsed_string = ansi_screen

    # replace the escape codes added by TheDraw
    # \033[?7h
    # \033[255D
    parsed_string = parsed_string.replace('\033[?7h', '')
    parsed_string = parsed_string.replace('\033[255D', '')

    # Pattern to match escape codes in the ansi screen
    ansi_pattern = r"\033\[[0-9;]+m"
    ansi_compiled_pattern = re.compile(ansi_pattern)

    # tokenized the ANSI codes
    tokens = ansi_compiled_pattern.finditer(parsed_string)

    # Iterate through the tokens (ANSI codes) and replace
    # then with evennia color tags
    for token in tokens:
        parsed_string = parsed_string.replace(token.group(), evennia_colors(token.group()), 1)

    # return the parsed string and add a final '|n' code
    return parsed_string + EVENNIA_ANSI_NORMAL


# Auxuliary function
def evennia_colors(ansi_code):
    """
    Translate the ANSI codes to evennia color tags
    """
    # Global variable for Moebious way to write ANSI code
    # when HILITE white
    global LAST_EC_PARSED

    colortag = ''

    # remove the escape code plus [ from ANSI codes
    ansi_code = ansi_code.replace(AU_ANSI_ESCAPE_COLOR, '')
    # remove the final m from ANSI codes
    ansi_code = ansi_code.replace('m', '')

    # split the terms of the ansi code
    codes = re.split(';', ansi_code)

    # Determine the amount of terms in the ANSI code
    terms = len(codes)

    # Convert te map in a dictionary
    ansi_map_dict = dict(ansi_map)

    # Do the actual replacement ANSI -> EVENNIA
    code = ''
    if terms == 1:
        if codes[0] == '0':
            colortag = ansi_map_dict[codes[0]]
        elif codes[0] == '1':
            colortag = ansi_map_dict[LAST_EC_PARSED + 'h']
        elif codes[0] == '4':
            colortag = ansi_map_dict[codes[0]]
        elif codes[0] == '5':
            colortag = ansi_map_dict[codes[0]]
        else:
            colortag = ansi_map_dict[codes[0]]
            LAST_EC_PARSED = codes[0]                       # Save the FOREGROUND color
    elif terms == 2:
        if codes[0] == '0':
            for code in codes:
                colortag = colortag + ansi_map_dict[code]

            LAST_EC_PARSED = codes[1]                       # Save the FOREGROUND color
        elif codes[0] == '1':
            colortag = ansi_map_dict[codes[1] + 'h']

            LAST_EC_PARSED = codes[1]                       # Save the FOREGROUND color
        elif codes[0] == '4':
            for code in codes:
                colortag = colortag + ansi_map_dict[code]

            LAST_EC_PARSED = codes[1]                       # Save the FOREGROUND color
        elif codes[0] == '5':
            for code in codes:
                colortag = colortag + ansi_map_dict[code]

            LAST_EC_PARSED = codes[1]                       # Save the FOREGROUND color
        else:
            for code in codes:
                colortag = colortag + ansi_map_dict[code]

            LAST_EC_PARSED = codes[0]                       # Save the FOREGROUND color
    elif terms >= 3:
        HI = ''
        for code in codes:
            if code == '1':
                HI ='h'
            else:
                if int(code) >= 30:
                    colortag = colortag + ansi_map_dict[code + HI]
                    HI = ''
                    if int(code < 40):
                        LAST_EC_PARSED = code
                else:
                    colortag = colortag + ansi_map_dict[code]
    else:
        pass

    return colortag
