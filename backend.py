import configparser
import os
import random
import sys
import discord
import logging
import inflect
import pathlib
from colorlog import ColoredFormatter


# Initializing the logger
def colorlogger(name: str = 'my-discord-bot') -> logging.log:
    logger = logging.getLogger(name)
    stream = logging.StreamHandler()

    stream.setFormatter(ColoredFormatter("%(reset)s%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s"))
    logger.addHandler(stream)
    return logger  # Return the logger


log = colorlogger()
p = inflect.engine()

# Loading config.ini
config = configparser.ConfigParser()

try:
    config.read('./data/config.ini')
except Exception as e:
    log.critical("Error reading the config.ini file. Error: " + str(e))
    sys.exit()

# Getting variables from config.ini
try:
    # Getting the variables from `[general]`
    log_level: str = config.get('general', 'log_level')
    presence: str = config.get('general', 'presence')

    # Getting the variables from `[secret]`
    discord_token: str = config.get('secret', 'discord_token')

    # Getting the variables from `[discord]`
    embed_footer: str = config.get('discord', 'embed_footer')
    sync_server: str = config.getint('discord', 'sync_server', fallback=0)
    should_sync: str = config.getboolean('discord', 'should_sync', fallback=False)
    embed_color: int = int(config.get('discord', 'embed_color'), base=16)
    embed_url: str = config.get('discord', 'embed_url')


except Exception as err:
    log.critical("Error getting variables from the config file. Error: " + str(err))
    sys.exit()

# Set the logger's log level to the one in the config file
if log_level.upper().strip() in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    log.setLevel(log_level.upper().strip())
else:
    log.setLevel("INFO")
    log.warning(f"Invalid log level `{log_level.upper().strip()}`. Defaulting to INFO.")


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

def name_init():
    """Initializes the name generation chains."""
    grouplen = 2  # length of groups made into chains
    out = dict()
    for namebase in os.listdir("data/name_generator"):
        def increment(lst, cur):
            if lst in list(chain.keys()):
                if cur in list(chain[lst].keys()):
                    chain[lst][cur] += 1
                else:
                    chain[lst][cur] = 1
            else:
                chain[lst] = dict()
                chain[lst][cur] = 1

        chain = dict()
        with open(os.path.join(namebase), 'r', encoding='utf8') as f:  # open in readonly mode
            lines = f.read().splitlines()
        for line in lines:
            grouping = [line[i:i + grouplen] for i in range(0, len(line), grouplen)]
            last = "#"
            for i in grouping:
                increment(last, i)
                last = i
            increment(last, "#")
        out[os.path.splitext(namebase)[0]] = chain
    return out

namechains = name_init()

def name_generator(kind: str, amount: int = 10) -> list[str]:
    """Generates a list of names. Defaults to 10."""
    chain = namechains[kind]
    out = []
    for _ in range(int(amount)):
        name = random.choices(list(chain["#"].keys()), weights=list(chain["#"].values()))
        while True:
            while True:
                name += random.choices(list(chain[name[-1]].keys()),
                                weights=list(chain[name[-1]].values()))
                if name[-1] == "#":
                    if random.random() < len(name) / 12 - 1 / 12:  # end it
                        break
                    else:
                        name = name[:-1]  # try again
                else:
                    if random.random() < len(name) / 24 - 1 / 24:  # end it
                        name += "#"
                        break
                    else:
                        break
            if len(name) == 12 or name[-1] == "#":
                break
        out.append(''.join(name).replace('#', ''))
    return out

def plural(text, num):
    """Wrapper for Inflect's automatic plurals."""
    return p.plural(text, num)
