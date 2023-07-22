import inflect

p = inflect.engine()


def plural(text, num):
    """Wrapper for Inflect's automatic plurals."""
    return p.plural(text, num)
