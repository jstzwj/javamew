
import unicodedata

IDENT_START_CATEGORIES = set(['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Nl', 'Pc', 'Sc'])

IDENT_PART_CATEGORIES = set(['Lu', 'Ll', 'Lt', 'Lm', 'Lo', 'Mc', 'Mn', 'Nd', 'Nl', 'Pc', 'Sc'])


def is_java_identifier_start(c):
    """
    Check if the given character is a Java identifier start character.
    """
    return unicodedata.category(c) in IDENT_START_CATEGORIES

def is_java_identifier_part(c):
    """
    Check if the given character is a Java identifier part character.
    """
    return unicodedata.category(c) in IDENT_PART_CATEGORIES
