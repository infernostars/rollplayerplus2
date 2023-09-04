import discord

from backend.config import embed_footer, embed_color, embed_url


def embed_template(title: str, description: str):
    """Creates an Embed with the default color with provided title and description."""
    _embed_template = discord.Embed(
        title=title,
        description=description,
        color=embed_color,
        url=embed_url
    )

    _embed_template.set_footer(text=embed_footer)
    return _embed_template.copy()


def error_template(description: str) -> discord.Embed:
    """Creates an Embed with a red color and an "error!" title."""
    _error_template = discord.Embed(
        title="Error!",
        description=description,
        color=0xff0000,
        url=embed_url
    )

    _error_template.set_footer(text=embed_footer)
    return _error_template.copy()