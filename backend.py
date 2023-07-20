import configparser
import random
import sys
import discord
import logging
import inflect
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


def greek_name_generator(amount: int = 10) -> list[str]:
    """Generates a list of greek names, defaults to 10."""
    nm1 = ["Ab", "Abd", "Ac", "Ach", "Act", "Aeg", "Aen", "Agrin", "Aig", "Akr", "Al", "Am", "Amar", "Amb", "Amph",
           "Andr", "Ank", "Ant", "Ap", "Aph", "Arg", "Ars", "Art", "As", "Ask", "Askl", "Asp", "Ass", "Ast", "Ath",
           "Ayt", "B", "Bar", "Bhryt", "Bor", "Bour", "Bouthr", "Braur", "Bubl", "Byll", "Byz", "Cal", "Car", "Cebr",
           "Ch", "Chalc", "Cham", "Chers", "Claz", "Cnid", "Col", "Cor", "Corc", "Crot", "Cum", "Cym", "Cyr", "Cyth",
           "D", "Dec", "Del", "Delph", "Dem", "Did", "Dim", "Dios", "Diosc", "Dod", "Dor", "Dym", "Ed", "El", "Elat",
           "Eleut", "Emp", "Ep", "Eph", "Epid", "Er", "Eres", "Eret", "Ereth", "Eretr", "Erythr", "Eub", "G", "Gangr",
           "Gaz", "Gel", "Golg", "Gonn", "Gorg", "Gort", "Gourn", "Gyth", "H", "Hal", "Hel", "Hell", "Hem", "Hemer",
           "Heracl", "Herm", "Hier", "Him", "Histr", "Hybl", "Hyel", "Ial", "Ias", "Id", "Imbr", "Iolc", "It", "Ith",
           "Jukt", "K", "Kall", "Kam", "Kamar", "Kameir", "Kann", "Kasm", "Kasmen", "Kat", "Kep", "Kerk", "Kimm",
           "Knid", "Knoss", "Kos", "Kour", "Kyd", "Kyr", "L", "Lam", "Lamps", "Laod", "Lap", "Lapith", "Lar", "Lat",
           "Leb", "Lefk", "Leib", "Leont", "Lepr", "Lind", "Lis", "Liss", "M", "Magn", "Mall", "Mant", "Mar", "Mass",
           "Meg", "Megal", "Mes", "Mess", "Met", "Meth", "Mil", "Mochl", "Mon", "Morg", "Myl", "Mynd", "Myon", "Myr",
           "Myrm", "Myt", "N", "Naucr", "Naup", "Nax", "Neap", "Nic", "Nicop", "Nir", "Nymph", "Nys", "Od", "Oen", "Ol",
           "Olb", "Olymp", "Olynth", "Onch", "Or", "Orch", "P", "Pag", "Pal", "Pand", "Pant", "Paph", "Par", "Patr",
           "Pavl", "Peir", "Pel", "Pell", "Perg", "Pets", "Phaist", "Phal", "Phan", "Phar", "Phas", "Pher", "Phil",
           "Phli", "Phoc", "Pin", "Pis", "Pith", "Pix", "Plat", "Pos", "Poseid", "Pot", "Prien", "Prous", "Ps",
           "Psychr", "Ptel", "Pydn", "Pyl", "Pyrg", "R", "Rhamn", "Rheg", "Rhith", "Rhod", "Rhyp", "Riz", "S", "Sal",
           "Sam", "Scidr", "Sel", "Sem", "Sest", "Seuth", "Sic", "Sid", "Sin", "Sit", "Sklav", "Smyrn", "Sol", "Soz",
           "Spart", "Stag", "Sten", "Stymph", "Syb", "Syr", "T", "Tan", "Tar", "Taur", "Teg", "Ten", "Thass", "Theb",
           "Theod", "Therm", "Thesp", "Thor", "Thron", "Thur", "Thyr", "Tom", "Tr", "Trag", "Trap", "Trip", "Troez",
           "Tyl", "Tyliss", "Tyr", "Vas", "Vath", "Zac", "Zakr", "Zancl"]
    nm2 = ["aca", "acia", "aclea", "actus", "acus", "acuse", "ada", "ae", "aea", "agas", "agoria", "agra", "ai",
           "aieus", "aikastro", "aion", "ais", "aistos", "aizi", "ake", "aki", "akros", "alamis", "ale", "alia", "alos",
           "amahos", "ame", "amea", "amis", "amnus", "amos", "ampos", "amum", "anais", "ane", "anes", "anos", "anthus",
           "antina", "antium", "apetra", "apeze", "apezus", "aphos", "apolis", "ara", "arae", "ares", "arina", "aris",
           "arnacia", "arnae", "arnassus", "aros", "arta", "asa", "asae", "aseia", "assa", "assus", "astiraki", "astro",
           "asus", "ateia", "athon", "atis", "atrae", "atrea", "auros", "aza", "ea", "ebes", "edon", "egea", "egion",
           "eia", "eidonia", "eion", "eira", "eiros", "ekion", "ela", "elea", "eleum", "elis", "embria", "emita", "ena",
           "enae", "enai", "endos", "ene", "eneia", "enes", "enia", "enimahos", "enion", "ens", "enus", "eos",
           "ephyrian", "epios", "era", "erae", "erikon", "erma", "erna", "eron", "eselis", "esia", "esmos", "esos",
           "espiae", "espontos", "essa", "essos", "estias", "esus", "ethra", "etra", "etri", "etria", "etrias", "etros",
           "etta", "etus", "eucia", "eum", "eus", "eusis", "eutherna", "eze", "ezus", "ia", "iae", "ias", "icapaeum",
           "icea", "icos", "icus", "icyon", "ida", "idaea", "ide", "idnae", "idon", "idos", "idrus", "iene", "igeneia",
           "igona", "igus", "ike", "iki", "ikon", "ila", "ilene", "iliki", "illai", "ina", "inda", "ine", "ini", "inia",
           "inion", "initida", "inope", "inth", "inus", "io", "ioch", "ion", "ione", "iopolis", "ios", "ipolis", "ippi",
           "ippia", "iraki", "iri", "is", "isos", "issa", "issos", "ita", "itake", "iteia", "ithos", "itida", "ium",
           "iunt", "ocaea", "odes", "odosia", "oe", "oezen", "ofa", "oinion", "oinon", "okampos", "olgi", "oli", "olis",
           "ollo", "ollonia", "omenion", "omenus", "omnos", "on", "ona", "onassa", "one", "onesos", "onia", "onion",
           "onnos", "ontos", "ontum", "ope", "opeion", "opetri", "opolis", "opus", "oria", "oricus", "orion", "orus",
           "os", "osia", "oskopeion", "osse", "ossos", "osthena", "otiri", "oton", "oupoli", "ous", "ousa", "ox", "oy",
           "urias", "urii", "urion", "us", "ussae", "ydna", "ydon", "ydos", "ylos", "yma", "ymna", "ympia", "yn",
           "ynthos", "ynthus", "ypes", "yra", "yras", "yreum", "yrgos", "yria", "yrian", "yrna", "yros", "ysos",
           "ysthenes", "ystus", "ythrae", "ytos"]
    a = random.choices(nm1, k=amount)
    b = random.choices(nm2, k=amount)
    return ["{}{}".format(a_, b_) for a_, b_ in zip(a, b)]


def plural(text, num):
    """Wrapper for Inflect's automatic plurals."""
    return p.plural(text, num)
